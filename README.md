# TeX2LMS
Python script to help create pools of questions on Blackboard LMS with LaTeX input stored in a spreadsheet. Each sheet of the spreadsheet is a pool of questions, each question is a row. LaTeX commands are converted into PNG images and the text is converted to an html reference to these images. The script then produces a tab-separated column text file, ready for import into the LMS.

## Database template 
For a multiple choice question (of MC type in blackboard) spreadsheet must contain at least the following headers

| Question Type | Question Title | Filename prefix | Description 1 | Answer 1 | Status 1 | Answer 2 | Status 2 |
| ------------- | -------------- | --------------- | ------------- | -------- | -------- | -------- | -------- |
| MC | A title | foldername | Some text describing the question | A correct answer | correct | A wrong answer | incorrect |

- The "Question Type" is code for LMS. Available options are detailed at https://help.blackboard.com/Learn/Instructor/Ultra/Tests_Pools_Surveys/Reuse_Questions/Upload_Questions
- The "Question Title" is for internal reference and ignored by LMS.
- The "Filename prefix" is both the folder name where the images of LaTeX are stored in, as well as a prefix to any files created for that question.
- "Description 1" is the question text. It can be plain text or LaTeX. Question descriptions can be split into many parts, i.e. "Description 1", "Description 2",..."Description n" for easier maintenance of small changes (versions). The script concatenates all columns starting with "Description " together before converting LaTeX to PNG images.
- "Answer j" is the jth answer to the multiple choice and "Status j" is either "correct" or "incorrect".


## **Important**

After importing the tab-separated column text file into the LMS, you **must manually edit the questions** (one-by-one) on LMS so that the links to the images are updated with links accessible to students. Indeed, every image/file stored in the Content Collection has two urls; the url corresponding to the natural location on the server (which the TeX2LMS script uses) and a cryptic alias shown only to students. For students to see the PNG images of a question, the cryptic alias is to be used. LMS automatically updates urls, but the process is only triggered upon manual editting of individual questions.
