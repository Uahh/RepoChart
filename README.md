<p align="center">
  <img src="static/you128.ico" width="128" height="128"/>
</p>

<div align="center">
  
# RepoChart

#### Visualize repositories on Github

</div>

## What's this
This project can graphically display the history, development, and current status of a repository.  
I posted the service on here:  https://uahh.site/repochart
  
## Charts introduction
I will use this project to introduce the charts of this project.  

### Circle Chart:
The chart reflect the importance of file in the repository.  
Each circle represents the total number of commits or total modified lines of the file in the repository.  
  
Order by total modified:  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/circle_chart_line.png" width="75%" height="75%">  
  
Order by number of commits:  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/circle_chart_line.png" width="75%" height="75%">  

### Files Size Chart and Sunset Chart:
The chart reflect the size of file in the repository.  
  
Files size chart:  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/square_chart.png" width="75%" height="75%">  
  
Sunset chart:  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/sunset_chart.png" width="75%" height="75%">  

### File Type Size Pie Chart:
The chart reflect the file type size percentage of the latest commits in the repository.  
  
Ring chart:  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/ring_chart.png" width="75%" height="75%">  
  
Pie chart:  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/pie_chart.png" width="75%" height="75%">  

### Active Chart:
The chart reflects the activity level of the repository.
  
Active chart:  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/active_line_chart.png" width="75%" height="75%">  

### Commit line Chart:
  
The chart reflect the file type size of latest commit in the repository.  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/commit_line_chart.png" width="75%" height="75%">  

### Star History Chart:
View the repository star history.  
Only the first 40k stars of the project can be displayed.  
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/star_history_chart.png" width="75%" height="75%">  

### Line Of Code Chart:
View the repository total lines of code.
  
<img src="https://github.com/Uahh/Repochart/blob/main/data/lines_of_code_chart.png" width="75%" height="75%">  


## Build locally
### Environment
Windows/Mac/Linux  
Only need Python3.x.  

### Step
1. Clone this repo:
```bash
git clone https://github.com/Uahh/RepoChart
cd RepoChart
```
2. Install dependent libraries:
```bash
pip install -r requirement.txt
```
3. In order to use github api to get star history, please apply for a token for your github account.  
You can follow this link:  
[Creating a personal token](https://docs.github.com/cn/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)  
  
4. Copy your token and paste in "models/github/private_config.py":
```python
token = "Your token"
```
5. Start making the repo chart you want:
```bash
python repochart_cli.py -r User/Repo
```
6. Start the server, Modify "192.168.31.11" to your local IP address:
```bash
python app.py --host 192.168.31.11:52173 --http
```
7. Visit http://192.168.31.11:52173 to view the charts.  
  
