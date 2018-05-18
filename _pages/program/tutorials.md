---
title: Tutorials
layout: single
excerpt: "EMNLP 2018 Tutorials."
permalink: /program/tutorials/
sidebar: 
    nav: "program"
---
{% include base_path %}

The following tutorials have been accepted for EMNLP 2018 and will be held as half-day sessions either on Wednesday, October 31, 2018 or on Thursday, November 1, 2018. Exact timings will be posted later as part of the official program.


<strong>T1: Deep Latent Variable Models of Natural Language</strong><br/>
<a href="http://people.seas.harvard.edu/~srush">Alexander Rush</a>, <a href="http://www.people.fas.harvard.edu/~yoonkim">Yoon Kim</a>, and <a href="https://swiseman.github.io">Sam Wiseman</a>

<div>
<p>The proposed tutorial will cover deep latent variable models both in the case where exact inference over the latent variables is tractable and when it is not. The former case includes neural extensions of unsupervised tagging and parsing models. Our discussion of the latter case, where inference cannot be performed tractably, will restrict itself to continuous latent variables. In particular, we will discuss recent developments both in neural variational inference (e.g., relating to Variational Auto-encoders) and in implicit density modeling (e.g., relating to Generative Adversarial Networks). We will highlight the challenges of applying these families of methods to NLP problems, and discuss recent successes and best practices.</p>
</div>

<strong>T2: Deep Chit-Chat: Deep Learning for ChatBots</strong><br/>
<a href="https://www.microsoft.com/en-us/research/people/wuwei">Wei Wu</a> and <a href="http://www.ruiyan.me">Rui Yan</a>

<div>
<p>The tutorial is based on the long-term efforts on building conversational models with deep learning approaches for chatbots. We will summarize the fundamental challenges in modeling open domain dialogues, clarify the difference from modeling goal-oriented dialogues, and give an overview of state-of-the-art methods for open domain conversation including both retrieval-based methods and generation-based methods. In addition to these, our tutorial will also cover some new trends of research of chatbots, such as how to design a reasonable evaluation system and how to "control" conversations from a chatbot with some specific information such as personas, styles, and emotions, etc.</p>
</div>

<strong>T3: Writing Code for NLP Research</strong><br/>
<a href="http://www.cs.cmu.edu/~mg1">Matt Gardner</a>, <a href="http://markneumann.xyz">Mark Neumann</a>, <a href="http://joelgrus.com">Joel Grus</a>, and <a href="https://www.linkedin.com/in/nicholaslourie">Nicholas Lourie</a>

<div>
<p>Doing modern NLP research requires writing code. Good code enables fast prototyping, easy debugging, controlled experiments, and accessible visualizations that help researchers understand what a model is doing. Bad code leads to research that is at best hard to reproduce and extend, and at worst simply incorrect. Indeed, there is a growing recognition of the importance of having good tools to assist good research in our field, as the upcoming workshop on open source software for NLP demonstrates. This tutorial aims to share best practices for writing code for NLP research, drawing on the instructors' experience designing the recently-released AllenNLP toolkit, a PyTorch-based library for deep learning NLP research. We will explain how a library with the right abstractions and components enables better code and better science, using models implemented in AllenNLP as examples. Participants will learn how to write research code in a way that facilitates good science and easy experimentation, regardless of what framework they use.</p>
</div>

<strong>T4: Joint models for NLP</strong><br/>
<a href="http://people.sutd.edu.sg/~yue_zhang/">Yue Zhang</a>

<div>
<p>Joint models have received much research attention in NLP, allowing relevant tasks to share common information while avoiding error propagation in multi-stage pepelines. Several main approaches have been taken by statistical joint modeling, while neual models allow parameter sharing and adversarial training. This tutorial reviews main approaches to joint modeling for both statistical and neural methods.</p>
</div>

<strong>T5: Graph Formalisms for Meaning Representations</strong><br/>
<a href="http://alopez.github.io/">Adam Lopez</a> and <a href="http://homepages.inf.ed.ac.uk/s1459276/">Sorcha Gilroy</a>

<div>
<p>In this tutorial we will focus on Hyperedge Replacement Languages (HRL; Drewes et al. 1997), a context-free graph rewriting system. HRL are one of the most popular graph formalisms to be studied in NLP (Chiang et al., 2013; Peng et al., 2015; Bauer and Rambow, 2016). We will discuss HRL by formally defining them, studying several examples, discussing their properties, and providing exercises for the tutorial. While HRL have been used in NLP in the past, there is some speculation that they are more expressive than is necessary for graphs representing natural language (Drewes, 2017). Part of our own research has been exploring what restrictions of HRL could yield languages that are more useful for NLP and also those that have desirable properties for NLP models, such as being closed under intersection. </p>

<p>With that in mind, we also plan to discuss Regular Graph Languages (RGL; Courcelle 1991), a subfamily of HRL which are closed under intersection. The definition of RGL is relatively simple after being introduced to HRL. We do not plan on discussing any proofs of why RGL are also a subfamily of MSOL, as described in Gilroy et al. (2017b). We will briefly mention the other formalisms shown in Figure 1 such as MSOL and DAGAL but this will focus on their properties rather than any formal definitions.</p>
</div>

<strong>T6: Standardized Tests as benchmarks for Artificial Intelligence</strong><br/>
<a href="https://sites.google.com/site/mrinsachan/">Mrinmaya Sachan</a>, <a href="https://seominjoon.github.io/">Minjoon Seo</a>, <a href="http://ssli.ee.washington.edu/~hannaneh/">Hannaneh Hajishirzi</a>, and <a href="http://www.cs.cmu.edu/~epxing/">Eric Xing</a>

<div>
<p>Standardized tests have recently been proposed as replacements to the Turing test as a driver for progress in AI (Clark, 2015). These include tests on understanding passages and stories and answering questions about them (Richardson et al., 2013; Rajpurkar et al., 2016a, inter alia), science question answering (Schoenick et al., 2016, inter alia), algebra word problems (Kushman et al., 2014, inter alia), geometry problems (Seo et al., 2015; Sachan et al., 2016), visual question answering (Antol et al., 2015), etc. Many of these tests require sophisticated understanding of the world, aiming to push the boundaries of AI. </p>

<p>For this tutorial, we broadly categorize these tests into two categories: open domain tests such as reading comprehensions and elementary school tests where the goal is to find the support for an answer from the student curriculum, and closed domain tests such as intermediate level math and science tests (algebra, geometry, Newtonian physics problems, etc.). Unlike open domain tests, closed domain tests require the system to have significant domain knowledge and reasoning capabilities. For example, geometry questions typically involve a number of geometry primitives (lines, quadrilaterals, circles, etc) and require students to use axioms and theorems of geometry (Pythagoras theorem, alternating angles, etc) to solve them. These closed domains often have a formal logical basis and the question can be mapped to a formal language by semantic parsing. The formal question representation can then provided as an input to an expert system to solve the question.</p>
</div>

