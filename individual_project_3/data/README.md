# Project 3 - Data guide

**DASC 3230**

## 1. HTRU2

File: `htru2_small.npz`. Each row is a radio-signal candidate from the
High Time Resolution Universe survey, described by four precomputed features.
Labels: 0 = background (non-pulsar), 1 = pulsar.

| Feature column, in order | Description |
|---|---|
| `profile_mean` | Mean of the integrated pulse profile |
| `profile_std` | Standard deviation of the integrated pulse profile |
| `dm_snr_mean` | Mean of the DM-SNR curve |
| `dm_snr_std` | Standard deviation of the DM-SNR curve |

| Main arrays | Rows | Background | Pulsar |
|---|---:|---:|---:|
| `X_train, y_train` | 1,650 | 1,500 | 150 |
| `X_calibration` | 400 | 400 | 0 |
| `X_test, y_test` | 900 | 800 | 100 |

Source: [HTRU2, UCI (Lyon, 2015)](https://archive.ics.uci.edu/dataset/372/htru2).
CC BY 4.0.

## 2. Fashion-MNIST

File: `fashion_small.npz`. Images are 28 x 28 grayscale product images,
stored as uint8 values from 0 to 255. Each image has one label.

Labels: 0 = T-shirt/top, 1 = Trouser, 2 = Bag.

| Main arrays | Images | Per class |
|---|---:|---:|
| `images_train, labels_train` | 1,200 | 400 |
| `images_val, labels_val` | 300 | 100 |
| `images_test, labels_test` | 600 | 200 |

Train/validation: official training set. Test: official test set.

Source: [Fashion-MNIST, Zalando Research (2017)](https://github.com/zalandoresearch/fashion-mnist).
MIT.
