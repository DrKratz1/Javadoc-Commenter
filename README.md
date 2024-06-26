Latest 05/05/24
# JavaDoc Commenter

Hello everyone! I have taken it upon myself to write a semi-automatic Javadoc Commenter which will generate 2 files for convenient management of all JavaDoc related comments for 
any directory. Currently, it does not have a file recurse implementation so if you, the user, wants to utilize this tool on subdirectories, feel free to add your own implementation 
(if you do so, please create a fork and ask for merge). 




## **IMPORTANT**

This will add 2 files: function.csv and parameters.csv, which will be the data storage for program when running to auto comment your files.
This is purely a commenter and will not add nor remove any code - think of this as a sort of auto-formatter such as prettier.
When using this tool and editing the csv files, it is highly recommended to get an extension such as Rainbow CSV to help identify the columns

As I'm working off of VSCode, I will linke the extension I use:

Rainbow CSV: https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv




## **Usage**
1. Download the Commenter.py file, and copy it into your "src" folder where you want it to run on all the .java files.
2. Make sure that you have Python installed (as long as its Python 3 it will be fine)
3. In the terminal, check that the current working directory is the "src" folder - ie. path something like: C:\Users\...\...project-2\src.

	3.1 If this is not the case, then use the "cd" commmand to the path into that form - e.g. path is C:\Users\...\...project-2 -> then type "cd src" into terminal and it will be in the 				correct path

4. Then, run the program with "python Commenter.py" for Windows - I'm not too sure what the equivalent is for Mac/Linux - look online for this
   
5. It should prompt you to type in either "1" or "2" or "3".
 
	5.1 "1" will read all your .java files and generate the 2 storage csv files.
   
	5.2 If files don't immediately show up, close and reopen your IDE.
   
	5.3 Add explanations to "parameters.csv" **WITH NO SPACE AFTER THE COMMA** like so:
   
   ![image](https://github.com/DrKratz1/Javadoc-Commenter/assets/141234325/78fd37dc-9bf0-48ea-a803-198da504fd51)

	5.4 Similarly, do so for "functions.csv" but add explanation of the function in the column for "Explanation" and explanation of the return type under "ReturnExplanation.
   		An example filled in row could be:

   ![image](https://github.com/DrKratz1/Javadoc-Commenter/assets/141234325/56326b2b-11f4-40d2-bd2a-b505ac53b914)

6. Once all data has been filled in, rerun the code and type "2" then press enter. This will add in JavaDoc comments to your code.

7. All done!

8. (Optional) If you would like to take out all JavaDoc Comments, type "3" and it will delete **EVERY JAVADOC COMMENT MADE** - make sure you have all JavaDoc related comments backed up into generated csv files.




## **Issues**

If your function is structured like this: "visibilityModifier returnType functionName(parameters);" - it will not detect it and will ignore it when rewriting, the fix for this is just 
to add in the "abstract" keyword into the line and it will now detect it and add comments to it.




## **Future Features**

Making GUI

Recursively going through folders to locate .java files

Reading in existing doc comments to csv storages

REFACTOR CODE

Add ability to ignore files for files that you don't want commented, or changed by program in anyway




## **Contributing**
First of all - apologies for the code being quite questionable - it was written on the principle of get it to work then think about if I want to make it cleaner later (also if you can't tell I'm not the greatest programmer). If you would like to contribute, thank you, and please look into either **Issues** for things to fix or **Future Features** to implement new ideas. If you have any new ideas about the project, feel free to do so, and if they are overall beneficial, then I will add them.

Honestly I don't expect this project to become anything large, but if anyone at all decides to care and contribute it would make my day <3.




## **Changelog**

02/05 - Initial version uploaded

05/05 - Updated to put comments directly into .java files and added doc removal functionality
