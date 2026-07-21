# Project Overview

## 1. Project Title

Agentic-image-analyser

## 2. Summary

An agentic system that captions uploaded images using a PyTorch vision model, then autonomously decides whether additional research is needed to produce a genuinely useful report - rather than stopping at a single-line caption. 

The agent's reasoning is powered by a self-hosted LLM (via Ollama) and orchestrated using LangGraph

## 3. Problem Statement

A standard image captioning model can describe what's visually in an imiage, but it can't reason about that description or decide what to do next - it produces a single caption and stops.

This project builds an agent that goes further - it decides for itself whether the caption alone is sufficient, or whether additional context (such as a web search) is needed to provide a useful informative report - rather than a fixed, hardcoded sequence of steps.

Building this system that reasons about its next steps is a meaningfully more advanced patterns, closer to how real production AI agents are built.

## 4. Project Objectives

The main objectives of this project are to:

- Create a PyTorch image captioning model
- Build a multi-step agent capable of deciding its own next action, rather than following a fixed pipeline
- Self-host an open-source LLM locally (via Ollama) instead of relying on a paid third-party API
- Orchestrate the agent's tool use (captioning, web search) using LangGraph

## 5. Target Users

The primary users of this system are:

1. Someone wanting a quick, informative summary of an image (not just a one-line description)
2. A computer science enthusiast evaluating this project demonstrating agentic AI system design

## 6. Project Constraints

- Hardware constraint: no dedicated NVIDIA GPU available, which rules out vLLM and shaped the choice of Ollama
- Technology constraint: limited to open-source, locally runnable models to avoid ongoing API costs
- Knowledge Constraint: first project using LangGraph and agent orchestration, so some learning curve is expected



