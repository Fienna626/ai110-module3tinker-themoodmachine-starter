# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
I compared both models. The core system is rule based (`mood_analyzer.py`) and I also ran the ML pipeline in `ml_experiments.py`.

**Intended purpose:**  
Classify short social-media style posts into mood categories: positive, negative, neutral, or mixed.

**How it works (brief):**  
- Rule based: preprocesses text to tokens, matches against positive/negative lexicons, applies a simple negation rule (`not X` flips polarity), and adds emoji rules; then maps final score to a label.
- ML: trains `LogisticRegression` on bag-of-words vectors created by `CountVectorizer` from the same posts and labels.


## 2. Data

**Dataset description:**  
`SAMPLE_POSTS` has 17 posts after expansion (original 14 + 3 new). Posts include everyday phrases, slang, emojis, sarcasm-like statements, and mixed-emotion lines.

**Labeling process:**  
I manually assigned `TRUE_LABELS` to match the intended tone. New posts:
- "This is awesome!" -> positive
- "Feeling meh about everything" -> neutral
- "Super pumped for the party 🎉" -> positive

Posts hard to label:
- "Lowkey stressed but kind of proud of myself" (mixed)
- "Highkey excited but also nervous about tomorrow" (mixed)
- "I absolutely love getting stuck in traffic" (negative because sarcastic meaning)

**Important characteristics of your dataset:**  
- Contains slang ("lowkey", "highkey", "no cap")
- Contains emojis (":)", "🔥", "💀", "🎉")
- Contains expressed mixed feelings and ambiguity
- Includes sarcasm candidate: "I absolutely love getting stuck in traffic"

**Possible issues with the dataset:**  
- Small size (17 samples) and limited lexical coverage.
- Label categories are unbalanced with mostly positive/neutral; mixed is fewer.
- Contains informal text; may not generalize to formal writing.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
- Preprocess: lowercasing, trimming whitespace, splitting by whitespace.
- Removed punctuation in an earlier iteration but kept emoji tokens by preserving non-word content.
- Positive words from `POSITIVE_WORDS`; negative words from `NEGATIVE_WORDS`.
- Negation: if token == "not" and next token is in positive/negative (or emoji), flip the sign.
- Emoji handling: "+1" for [":)", "🙂", "😂", "🔥", "🎉"], "-1" for ["💀", ":(", "🥲"].
- Score to label: >0 positive, <0 negative, 0 neutral.

**Strengths of this approach:**  
- Easy to understand and debug.
- Predictable behavior on literal sentiment words.
- Works fast and without external dependencies beyond core Python.

**Weaknesses of this approach:**  
- Fails at sarcasm: "I absolutely love getting stuck in traffic" was predicted positive because "love" is positive (no sarcasm detection).
- Mixed mood detection is approximate and skewed by strong words: e.g., "Feeling tired but kind of hopeful" predicted negative (tired dominates).
- Slang outside lexicons or word mismatch: "sick" was ignored as neutral.
- Does not handle complex grammatical structures, intensity, or context beyond single-token rule flips.

## 4. How the ML Model Works (if used)

**Features used:**  
Bag-of-words using `CountVectorizer`.

**Training data:**  
Trains on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**  
- On the existing set, ML achieved 1.00 accuracy due to overfitting on 17 examples.
- It learned co-occurrence patterns such as "love" + "traffic" being negative in this small dataset.

**Strengths and weaknesses:**  
- Strength: can automatically infer patterns from the exact dataset (e.g., mixed/irony cues from combinations).
- Weakness: high risk of overfitting and poor generalization with limited data; sensitive to label changes.

## 5. Evaluation

**How you evaluated the model:**  
- Rule-based: `python main.py` prints predicted vs true labels and accuracy.
- ML: `python ml_experiments.py` prints predicted vs true labels and accuracy, plus an interactive mode.

**Examples of correct predictions:**  
- "Today was a terrible day" -> negative
- "So excited for the weekend" -> positive
- "Oh great, another meeting 💀" -> negative

**Examples of incorrect predictions:**  
- Rule-based: "I absolutely love getting stuck in traffic" predicted positive, true negative (sarcasm and conflicting context ignored).
- Rule-based: "Feeling tired but kind of hopeful" predicted negative, true mixed (one strong negative token suppressed mix).
- Rule-based: "This party is sick" predicted neutral ("sick" not in word lists).
- ML: no errors on training data (accuracy 1.00), but this may hide generalization failures.

## 6. Limitations

- Very small training dataset (17 samples) means even ML can overfit.
- Rule-based model cannot reliably detect sarcasm; example: positive token "love" wins in "I absolutely love getting stuck in traffic".
- Mixed mood patterns are handled by ad-hoc scoring and can be incorrect when one keyword dominates.
- Slang words not in `POSITIVE_WORDS`/`NEGATIVE_WORDS` are ignored, e.g. "sick" or "fire" except manual handling for some emoji.
- Language bias: dataset is U.S.-centric casual internet style, may misinterpret dialects, code-switching, or non-Western expressions.

## 7. Ethical Considerations

- Mood classification can impact users if applied to mental health or moderation; misclassifying distress as neutral/positive is risky.
- The data includes slang and informal tone; this favors some groups over others and may systematically misinterpret non-standard English forms.
- Privacy: using such a model on personal messages requires explicit consent and secure handling.

## 8. Ideas for Improvement

- Add significantly more labeled data across speakers, dialects, and context types.
- Use TF-IDF or word embeddings (e.g., sentence-transformers) for richer features.
- Add explicit sarcasm detection rules (e.g., common sarcastic trigger patterns) or a separate sarcasm classifier.
- Improve preprocessing with better emoji support, repeated character normalization, and multi-word phrase detection.
- For rule-based: add mixed thresholds (e.g., score == 1 or -1 map to mixed) and explicit phrase lists.
- Introduce a held-out test set to avoid reporting training accuracy as final performance.

**Your scoring rules:**  
Describe the modeling choices you made.  
Examples:  

- How positive and negative words affect score  
- Negation rules you added  
- Weighted words  
- Emoji handling  
- Threshold decisions for labels

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?

**Weaknesses of this approach:**  
Where does it fail?  
Examples: sarcasm, subtlety, mixed moods, unfamiliar slang.

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

## 5. Evaluation

**How you evaluated the model:**  
Both versions can be evaluated on the labeled posts in `dataset.py`.  
Describe what accuracy you observed.

**Examples of correct predictions:**  
Provide 2 or 3 examples and explain why they were correct.

**Examples of incorrect predictions:**  
Provide 2 or 3 examples and explain why the model made a mistake.  
If you used both models, show how their failures differed.

## 6. Limitations

Describe the most important limitations.  
Examples:  

- The dataset is small  
- The model does not generalize to longer posts  
- It cannot detect sarcasm reliably  
- It depends heavily on the words you chose or labeled

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  
Examples: 

- Misclassifying a message expressing distress  
- Misinterpreting mood for certain language communities  
- Privacy considerations if analyzing personal messages

## 8. Ideas for Improvement

List ways to improve either model.  
Possible directions:  

- Add more labeled data  
- Use TF IDF instead of CountVectorizer  
- Add better preprocessing for emojis or slang  
- Use a small neural network or transformer model  
- Improve the rule based scoring method  
- Add a real test set instead of training accuracy only
