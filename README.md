```markdown
<div align="center">

# ⚡ Serverless Image Optimization Pipeline

### Automatically compress, resize & convert images to WebP — powered by AWS

[![AWS SAM](https://img.shields.io/badge/AWS%20SAM-Serverless-orange?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/serverless/sam/)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)](https://aws.amazon.com/lambda/)
[![S3](https://img.shields.io/badge/Amazon-S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> Drop a 4MB photo in. Get a 80KB WebP out. Automatically. In under a second.

<br/>

</div>

---

## 🧩 The Problem

Modern apps are drowning in raw images. Users upload massive smartphone photos — 3 to 8 MB each. Serving those originals to mobile users means:

- 🐢 Slow load times → higher bounce rates
- 💸 Expensive bandwidth bills at scale
- 📱 Terrible experience on 4G/5G networks
- 🔧 Developers manually compressing assets

---

## ✅ The Solution

A **fully serverless, event-driven pipeline** that intercepts every upload, optimizes it, and stores a mobile-ready version — with zero human involvement.

```
Upload JPEG/PNG  →  S3 Trigger  →  Lambda (Pillow)  →  Optimized WebP
     4 MB        →   instant    →   resize + convert  →    ~80 KB
```

---

## 🏗️ Architecture

```
┌─────────────┐     s3:ObjectCreated      ┌──────────────────┐
│   Developer  │ ──── raw-uploads/ ──────▶ │   AWS Lambda     │
│   / App      │                           │   Python 3.13    │
└─────────────┘                           │   + Pillow        │
                                          └────────┬─────────┘
                                                   │
                                          resize + convert
                                          to WebP (quality 80)
                                                   │
                                                   ▼
                                    ┌──────────────────────────┐
                                    │  S3: optimized-delivery/ │
                                    │  filename.webp (~80KB)   │
                                    └──────────────────────────┘
```

| Layer | Service | Purpose |
|---|---|---|
| Storage | Amazon S3 | Receives uploads, stores output |
| Compute | AWS Lambda | Runs image processing code |
| Trigger | S3 Event Notification | Fires Lambda on every upload |
| IaC | AWS SAM + CloudFormation | Deploys entire stack in one command |
| Permissions | AWS IAM | Least-privilege read/write access |
| Image Engine | Pillow (PIL) | Resize, convert, compress |

---

## ✨ Features

- 🚀 **Zero infrastructure** — fully serverless, scales automatically
- 🔁 **Event-driven** — triggers instantly on every S3 upload
- 📐 **Smart resizing** — max 400px width, aspect ratio preserved
- 🖼️ **WebP conversion** — 25–34% smaller than JPEG at same quality
- 🔒 **Secure by default** — private bucket, least-privilege IAM
- ♾️ **Infinite loop safe** — skips already-optimized files
- 📊 **Observable** — full CloudWatch logging on every invocation

---

## 📁 Project Structure

```
mobile-image-optimizer/
│
├── template.yaml              # SAM/CloudFormation — all AWS resources
│
├── image_processor/
│   ├── app.py                 # Lambda handler — core processing logic
│   └── requirements.txt       # Python dependencies (Pillow)
│
└── Serverless_Image_Optimization_Pipeline.pdf   # Full technical documentation
```

---

## 🚀 Quick Start

### Prerequisites
- [AWS CLI](https://aws.amazon.com/cli/) configured (`aws configure`)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.13

### Deploy in 2 commands

```bash
sam build
sam deploy --guided
```

That's it. SAM provisions the S3 bucket, Lambda function, IAM roles, and event wiring automatically.

### Test it

```bash
# Upload any image to the raw-uploads/ prefix
aws s3 cp your-photo.jpg s3://<your-bucket>/raw-uploads/your-photo.jpg

# Watch the Lambda logs live
aws logs tail /aws/lambda/sam-app-image-optimizer --follow
```

Check your S3 bucket for the `optimized-delivery/` folder — your `.webp` file will be there within seconds.

---

## 📊 Real Test Results

| Metric | Before | After |
|---|---|---|
| File Size | ~4,000 KB | ~80 KB |
| Format | JPEG / PNG | WebP |
| Width | Full resolution | Max 400px |
| Processing Time | — | < 1 second |
| Human Effort | Manual | **Zero** |

---

## 🔮 Future Enhancements

- [ ] CloudFront CDN for global edge delivery
- [ ] Generate multiple sizes (thumbnail / mobile / desktop)
- [ ] SQS Dead-Letter Queue for failed retries
- [ ] SNS notifications on completion
- [ ] EXIF metadata extraction to DynamoDB

---

## 💰 Cost

Nearly free for most workloads.

- **Lambda** — first 1M requests/month are free
- **S3** — ~$0.023/GB/month storage
- **Example:** 100,000 images/month ≈ **under $0.25**

---

## 📄 Documentation

A full technical PDF is included in this repo covering architecture, IAM design, data flow, test results, and real-world use cases.

👉 [`Serverless_Image_Optimization_Pipeline.pdf`](./Serverless_Image_Optimization_Pipeline.pdf)

---

<div align="center">

Built with ❤️ using AWS SAM · Lambda · S3 · Python · Pillow

</div>
```
