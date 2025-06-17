
# TLDR

Honestly, the whole bulk downloading and script running thing is not worth it if you just want to see some diffs. Just do the quickstart way. If you do end up running the script, lmk if you run into any errors.

---

## Quickstart

- Grade as usual until you give a 100  
- Download this notebook and use it as the solution, for now (hacky, i know)
- Install the diff tool:
  ```bash
  pip install nbdime
  ```
- Compare notebooks:
  ```bash
  nbdiff-web solution.ipynb student.ipynb
  ```
- (asap) use the solution pdf, please don’t skip this

---

## Bulk Download

Honestly, it’s not worth the complexity, just manually download each nb. But if you really want to…

1. On Codio, go to the course Overview page, click the 3 dots next to the assignment and select **“Export Assignment Data”**. You’ll get an email link eventually.
2. Download and extract the file.  
   *(tip: you might have to shorten the file name)*
3. Edit and run the script. Scroll down to `__main__` and change these 2 lines:
   ```python
   ZIP_FOLDER = "assignment-3--train-decision-trees-after-data" 
   NOTEBOOK_NAME = "BuildADecisionTree.ipynb"  
   ```

**IMPORTANT:**  
Move the folder with all of the student zips into this `BTT_tool/` repo, just like you see with `assignment-3`. The script expects this structure, and it prevents an error saying the file name is too long.

The script:
- Extracts all of the student zips
- Moves them all to a folder titled `aaa_submissions`
- Reorders them by last name  
  *(note: some students have multi-part names which messes up the final nb order a bit)*

---

### The end result is:

```
assignment-3--train-decision-trees-after-data-preparation/
├── aaa_submissions/
│   ├── BuildADecisionTree_student1.ipynb
│   ├── …
│   └── BuildADecisionTree_student60.ipynb
├── student folders
├── …
├── student zip files
Extract_all_zips.py
README.md
```

---

## Solution.ipynb

In either case, the most tedious part is the solution nb – I manually copy and paste each cell from the pdf (hope Melissa can help skip this step). It’s even harder if you want the output cells to be exact. You have to:

- Do the bulk download (since it downloads the dataset and virtual env too)
- Copy and run the solution nb and hope you get no errors

---

## BTW

I was trying to create some automatic testing, but only the zip extracting is working so far. If you’re able to run the solution nb without error (especially for the labs because those notebooks are more complicated, and thus more likely to fail), I would be really interested to hear how you did it. The problem is likely that I ran it in my local env instead of the venv. At least my testing framework works, assuming all cells in the nb run.
