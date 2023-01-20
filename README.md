# SimplyGoCalculator
Q: What is this, and what is it for? 
</br>
A: This is a simple python script run in the command line that users can execute, on a monthly basis, to automatically calculate the total amount of money spent on public transportation in Singapore. 
</br>
</br>
Q: How do I use this?
</br>
A: Simply:
1) Pull the script from this repository 
2) Edit the fields indicated below 
3) Ensure that the packages stated in the requirements.txt file are installed in your environment
4) Execute the script monthly and get notified on the total amount spent on public transportation :smile:


## Table of Contents
- [Installation](https://github.com/crazzeex/simply_go_calculator/edit/main/README.md#installation)
- [Lines of code to change in the script](https://github.com/crazzeex/simply_go_calculator/edit/main/README.md#lines-of-code-to-change-in-the-script)
- [Documentation for Underlying Libraries](https://github.com/crazzeex/simply_go_calculator/edit/main/README.md#documentation-for-underlying-libraries)

### Installation
```
pip install -r requirements.txt
```

### Lines of code to change in the script

1) Line 40 - Replace <username> with your own username to simplygo
```
username_box.send_keys('<username>') 
```
2) Line 41 - Replace <password> with your own password to simplygo
```
password_box.send_keys('<password>')
```
3) Line 53 - Replace with the label of your credit card (refer to the text in the dropdown box)
```
dropdown.select_by_visible_text("<label of credit card>")
```
4) Line 126 - Replace with your path to the Downloads directory (default path should be as shown, with the user changed to your user profile) 
```
os.chdir(r'C:\Users\<user>\Downloads')  
```
5) Line 127 - Replace with your path to the Downloads directory (default path should be as shown, with the user changed to your user profile)
```
downloads_folder = os.listdir(r'C:\Users\<user>\Downloads')
```

### Documentation for underlying libraries
- [PDFQuery](https://github.com/jcushman/pdfquery#id2)
