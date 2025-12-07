# Roboflow Integration (serverless workflow)

This file documents the Roboflow serverless workflow used in the project. The integration code and API key were provided by the ML teammate — keep keys out of the public repo (store in env vars).

**Date:** 2025-12-04
**Author:** Shrinidhi Katti

## Summary
- Workspace: `ecoinnovatorssolarproject`
- Workflow ID: `find-solars-and-panels`
- Serverless endpoint base: `https://serverless.roboflow.com`

## How it is used in pipeline
1. Pipeline fetches satellite crop → saves JPG locally.
2. Pipeline calls Roboflow workflow (server-side) with image (URL or base64).
3. Roboflow returns predictions (masks, bboxes, confidences) and an optional base64 visualization image.
4. Pipeline consumes predictions to populate `<sample_id>.json` and create overlays.

## Example :
POST https://serverless.roboflow.com/ecoinnovatorssolarproject/workflows/find-solars-and-panels
Body: { "api_key": "", "inputs": { "image": {"type":"url","value":"https://.../img.jpg"}}}

## Expected response shape
A typical response includes `outputs[0].predictions` array and `outputs[0].visualization.value` (base64 image). The pipeline expects `class`, `confidence`, and `bbox/mask` fields in predictions.
