# -*- coding: utf-8 -*-
"""Experiments: SHAP stability for a sentiment classifier."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional

DEFAULT_SEED = 42
DEFAULT_MODEL = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"


@dataclass(frozen=True)
class DatasetBundle:
    name: str
    texts: list[str]
    labels: list[int]


def set_seed(seed: int) -> None:
    import random

    random.seed(seed)


def build_classifier(model_name: str = DEFAULT_MODEL, device: Optional[int] = None):
    from transformers import pipeline

    kwargs: dict[str, Any] = {"return_all_scores": True}
    if device is not None:
        kwargs["device"] = device
    return pipeline("sentiment-analysis", model=model_name, **kwargs)


def predict_proba(clf, texts: Iterable[str]):
import numpy as np

    outs = clf(list(texts), truncation=True)
    probs: list[list[float]] = []
    for o in outs:
        d = {x["label"].upper(): float(x["score"]) for x in o}
        probs.append([d.get("NEGATIVE", 0.0), d.get("POSITIVE", 0.0)])
    return np.asarray(probs, dtype=float)


def truncate_for_model(clf, text: str) -> str:
    max_tokens = getattr(clf.tokenizer, "model_max_length", 512) or 512
    if max_tokens > 10_000:
        max_tokens = 512
    ids = clf.tokenizer.encode(str(text), truncation=True, max_length=int(max_tokens))
    return clf.tokenizer.decode(ids, skip_special_tokens=True)


def prep_texts(clf, texts: Iterable[str]) -> list[str]:
    out: list[str] = []
    for t in texts:
        s = "" if t is None else str(t).strip()
        if s:
            out.append(truncate_for_model(clf, s))
    return out


def load_datasets(n_per_class: int = 300, seed: int = DEFAULT_SEED) -> list[DatasetBundle]:
    import pandas as pd
    from datasets import load_dataset

    def sample_tweeteval_binary(ds) -> tuple[list[str], list[int]]:
        df = ds["test"].to_pandas()
        df = df[df["label"].isin([0, 2])]
        neg = df[df["label"] == 0].sample(n_per_class, random_state=seed)
        pos = df[df["label"] == 2].sample(n_per_class, random_state=seed)
        out = (
            pd.concat([neg, pos], ignore_index=True)
            .sample(frac=1, random_state=seed)
            .reset_index(drop=True)
        )
        out["label"] = out["label"].map({0: 0, 2: 1})
        return out["text"].tolist(), out["label"].tolist()

    def sample_binary(ds, split: str = "test") -> tuple[list[str], list[int]]:
        df = ds[split].to_pandas()
        neg = df[df["label"] == 0].sample(n_per_class, random_state=seed)
        pos = df[df["label"] == 1].sample(n_per_class, random_state=seed)
        out = (
            pd.concat([neg, pos], ignore_index=True)
            .sample(frac=1, random_state=seed)
            .reset_index(drop=True)
        )
        return out["text"].tolist(), out["label"].tolist()

    ds_twitter = load_dataset("cardiffnlp/tweet_eval", "sentiment")
    ds_imdb = load_dataset("stanfordnlp/imdb")
    ds_amazon = load_dataset("SetFit/amazon_polarity")

    X_tw, y_tw = sample_tweeteval_binary(ds_twitter)
    X_im, y_im = sample_binary(ds_imdb, "test")
    X_am, y_am = sample_binary(ds_amazon, "test")

    return [
        DatasetBundle("twitter", X_tw, y_tw),
        DatasetBundle("imdb", X_im, y_im),
        DatasetBundle("amazon", X_am, y_am),
    ]


def build_global_explainer(clf):
    import shap

    masker = shap.maskers.Text(clf.tokenizer)

    def shap_model(texts):
        texts = prep_texts(clf, texts)
        probs = predict_proba(clf, texts)
        return probs[:, 1]

    return shap.Explainer(shap_model, masker, algorithm="partition")


def extract_token_importance(shap_values) -> list[tuple[str, float]]:
    import numpy as np

    tokens = shap_values.data
    vals = np.asarray(shap_values.values)
    if vals.ndim == 2 and vals.shape[1] == 1:
        vals = vals[:, 0]
    vals = np.abs(vals)
    pairs: list[tuple[str, float]] = []
    for t, v in zip(tokens, vals):
        if isinstance(t, str) and t.strip():
            pairs.append((t.lower(), float(v)))
    return pairs


def global_shap_scores(explainer, texts: list[str], max_samples: int = 20) -> dict[str, float]:
    import numpy as np
    from collections import defaultdict

    token_scores: dict[str, list[float]] = defaultdict(list)
    shap_values = explainer(texts[:max_samples])
    for sv in shap_values:
        for tok, val in extract_token_importance(sv):
            token_scores[tok].append(val)
    return {tok: float(np.mean(vs)) for tok, vs in token_scores.items()}


def top_k_tokens(global_shap: dict[str, float], k: int = 20) -> list[str]:
    return [t for t, _ in sorted(global_shap.items(), key=lambda x: -x[1])[:k]]


def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    a_set, b_set = set(a), set(b)
    return 0.0 if not (a_set or b_set) else len(a_set & b_set) / len(a_set | b_set)


def spearman_corr(a: dict[str, float], b: dict[str, float]) -> float:
from scipy.stats import spearmanr

    common = sorted(set(a) & set(b))
    if len(common) < 5:
        return float("nan")
    av = [a[t] for t in common]
    bv = [b[t] for t in common]
    corr = spearmanr(av, bv).correlation
    return float(corr) if corr is not None else float("nan")


def save_pickle(obj: Any, path: Path) -> None:
    import pickle

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(obj, f)


def run_global_stability(
    model: str = DEFAULT_MODEL,
    seed: int = DEFAULT_SEED,
    n_per_class: int = 300,
    max_samples: int = 20,
    device: Optional[int] = None,
) -> dict[str, Any]:
    set_seed(seed)
    datasets = load_datasets(n_per_class=n_per_class, seed=seed)
    clf = build_classifier(model, device=device)
    explainer = build_global_explainer(clf)

    global_scores: dict[str, dict[str, float]] = {}
    for ds in datasets:
        global_scores[ds.name] = global_shap_scores(
            explainer,
            prep_texts(clf, ds.texts),
            max_samples=max_samples,
        )

    tw, im, am = global_scores["twitter"], global_scores["imdb"], global_scores["amazon"]
    summary = {
        "jaccard@100": {
            "twitter-imdb": jaccard(top_k_tokens(tw, 100), top_k_tokens(im, 100)),
            "twitter-amazon": jaccard(top_k_tokens(tw, 100), top_k_tokens(am, 100)),
            "imdb-amazon": jaccard(top_k_tokens(im, 100), top_k_tokens(am, 100)),
        },
        "spearman": {
            "twitter-imdb": spearman_corr(tw, im),
            "twitter-amazon": spearman_corr(tw, am),
            "imdb-amazon": spearman_corr(im, am),
        },
    }
    return {"global_shap": global_scores, "summary": summary}


def main() -> int:
    import argparse
    import json

    p = argparse.ArgumentParser()
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--n-per-class", type=int, default=300)
    p.add_argument("--max-samples", type=int, default=20)
    p.add_argument("--device", type=int, default=None)
    p.add_argument("--out", type=Path, default=Path("artifacts/shap_experiment_artifacts.pkl"))
    args = p.parse_args()

    artifacts = run_global_stability(
        model=args.model,
        seed=args.seed,
        n_per_class=args.n_per_class,
        max_samples=args.max_samples,
        device=args.device,
    )
    save_pickle(artifacts, args.out)
    print(json.dumps(artifacts["summary"], indent=2))
    print(f"Saved: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())