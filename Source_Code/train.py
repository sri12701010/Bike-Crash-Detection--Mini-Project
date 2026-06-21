import argparse
from pathlib import Path

import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

from src.config import ModelConfig


def build_model(image_size: int, learning_rate: float) -> tf.keras.Model:
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(image_size, image_size, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(image_size, image_size, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
    )
    return model


def load_datasets(data_dir: Path, config: ModelConfig):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="binary",
        image_size=(config.image_size, config.image_size),
        batch_size=config.batch_size,
        validation_split=config.validation_split,
        subset="training",
        seed=42,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="binary",
        image_size=(config.image_size, config.image_size),
        batch_size=config.batch_size,
        validation_split=config.validation_split,
        subset="validation",
        seed=42,
    )

    class_names = train_ds.class_names
    print(f"[INFO] Class names: {class_names}")

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=autotune)
    val_ds = val_ds.prefetch(buffer_size=autotune)

    return train_ds, val_ds


def compute_weights_from_dataset(train_ds) -> dict:
    labels = []
    for _, y in train_ds.unbatch():
        labels.append(int(y.numpy()[0]))

    classes = np.unique(labels)
    weights = compute_class_weight(class_weight="balanced", classes=classes, y=labels)
    return {int(c): float(w) for c, w in zip(classes, weights)}


def train(data_dir: Path, model_out: Path, config: ModelConfig) -> None:
    train_ds, val_ds = load_datasets(data_dir, config)

    model = build_model(config.image_size, config.learning_rate)

    class_weights = compute_weights_from_dataset(train_ds)
    print(f"[INFO] Class weights: {class_weights}")

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(filepath=str(model_out), monitor="val_auc", mode="max", save_best_only=True),
    ]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=config.epochs,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    model_out.parent.mkdir(parents=True, exist_ok=True)
    model.save(model_out)
    print(f"[DONE] Model saved to {model_out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train bike crash classifier")
    parser.add_argument("--data-dir", type=Path, required=True, help="Path to processed frame dataset")
    parser.add_argument("--model-out", type=Path, required=True, help="Output model path (e.g., models/model.keras)")
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--image-size", type=int, default=224, help="Input image size")
    parser.add_argument("--learning-rate", type=float, default=1e-4, help="Learning rate")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg = ModelConfig(
        image_size=args.image_size,
        batch_size=args.batch_size,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
    )
    train(args.data_dir, args.model_out, cfg)
