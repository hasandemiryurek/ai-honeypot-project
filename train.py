#!/usr/bin/env python3
import sys
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

FEATURE_NAMES = [
    "bytecode_length", "f_hex_density", "call_opcode_count",
    "selfdestruct_count", "create_opcode_count", "sstore_count",
    "sload_count", "jump_density", "call_sstore_combo",
    "delegatecall_ratio", "ff_density", "loop_indicator",
]


def extract_features(bytecode: str) -> list:
    code = bytecode.replace("0x", "").lower()
    if len(code) < 4:
        return [0.0] * len(FEATURE_NAMES)

    bytes_list = [code[i:i+2] for i in range(0, len(code), 2)]
    total = len(bytes_list) or 1

    call_f1      = sum(1 for b in bytes_list if b == "f1")
    call_f2      = sum(1 for b in bytes_list if b == "f2")
    call_f4      = sum(1 for b in bytes_list if b == "f4")
    call_fa      = sum(1 for b in bytes_list if b == "fa")
    call_ops     = call_f1 + call_f2 + call_f4 + call_fa
    selfdestruct = sum(1 for b in bytes_list if b == "ff")
    create_ops   = sum(1 for b in bytes_list if b in ("f0", "f5"))
    sstore       = sum(1 for b in bytes_list if b == "55")
    sload        = sum(1 for b in bytes_list if b == "54")
    jumpi_count  = sum(1 for b in bytes_list if b == "57")
    jump_count   = sum(1 for b in bytes_list if b == "56")
    jump_density = (jump_count + jumpi_count) / total
    f_density    = code.count("f") / len(code)
    ff_density   = selfdestruct / total

    return [
        len(code), f_density, call_ops, selfdestruct, create_ops,
        sstore, sload, jump_density,
        1.0 if call_ops > 0 and sstore > 0 else 0.0,
        call_f4 / call_ops if call_ops > 0 else 0.0,
        ff_density,
        1.0 if jumpi_count / total > 0.05 else 0.0,
    ]


def main():
    print("=== Honeypot ML Model Trainer ===\n")
    try:
        df = pd.read_csv("mini_dataset.csv")
    except FileNotFoundError:
        print("ERROR: mini_dataset.csv bulunamadi"); sys.exit(1)

    print(f"Dataset: {len(df)} ornek")
    print(df["attack_type"].value_counts().to_string())
    print()

    X    = [extract_features(b) for b in df["bytecode"]]
    le   = LabelEncoder()
    y    = le.fit_transform(df["attack_type"].tolist())

    print("Siniflar:", list(le.classes_), "\n")

    model = RandomForestClassifier(
        n_estimators=300, max_depth=12, min_samples_leaf=1,
        class_weight="balanced", random_state=42, n_jobs=-1,
    )

    min_class_count = int(pd.Series(y).value_counts().min())
    n_splits = min(5, min_class_count)
    if n_splits >= 2:
     cv     = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
     scores = cross_val_score(model, X, y, cv=cv, scoring="f1_weighted")
     print(f"Cross-val F1 (weighted): {scores.mean():.3f} +/- {scores.std():.3f}\n")
    else:
     print("Cross-validation skipped: some classes have only 1 sample\n")

    model.fit(X, y)
    y_pred = model.predict(X)
    print(classification_report(y, y_pred, target_names=le.classes_))

    print("Feature importances:")
    for name, imp in sorted(zip(FEATURE_NAMES, model.feature_importances_),
                             key=lambda x: x[1], reverse=True):
        print(f"  {name:<26} {imp:.3f}  {'#' * int(imp * 40)}")

    joblib.dump({"model": model, "label_encoder": le}, "honeypot_ai_model.pkl")
    print("\nModel kaydedildi: honeypot_ai_model.pkl")


if __name__ == "__main__":
    main()