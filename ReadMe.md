# ACCforDI | Automatic Config Changer for Dynamic IP in [SCP: Secret Laboratory](https://scpslgame.com/)
<br>Dynamic IP detection isn't perfect in SL, thus I've written a script that's supposed to work as a crontab to detect the new IP and change it to the one you're using.

---
### This is _NOT_ an official tool from Northwood Studios! 
**Northwood is not responsible for any damage, and neither am I.**
**<br>You are fully responsible for using this tool. It's meant for files that are properly configured.**


---
## Installation

### Step 1 | Python
> - Install Python 3.7.8 or higher
> - Install the following dependencies:
<br>    - certifi^2021.10.8
<br>    - charset-normalizer^2.0.12
<br>    - idna^3.3
<br>    - requests^2.27.1
<br>    - urllib3^1.26.9
> - Change the `path` value inside the main.py file.
> - (Optional) Set a `webhook_url`, crontab does not save any logs.

### Step 2 | Scheduling the script execution
#### Linux (crontab)
> Add the following line to your crontab (`crontab -e` command)
> <br>It will execute the script every hour. Read the [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) documentation for more information.
> - `0 * * * *  python3 <path-to-file.py>`

#### Windows Server (SCHTASKS)
> Please read the [SCHTASKS](https://ss64.com/nt/schtasks.html) documentation for more information.
> <br>I didn't have a chance to schedule a task on Windows server yet, but I'm working on it.

#### Windows Client (Windows Task Scheduler)
> Please read this [article](https://techrando.com/2019/06/22/how-to-execute-a-task-hourly-in-task-scheduler/) for more information.
> <br>There's also a [stackoverflow](https://stackoverflow.com/questions/4249542/run-a-task-every-x-minutes-with-windows-task-scheduler) question about this.

---
##### Made by Wafel#8871 for [SCP: Secret Laboratory](https://scpslgame.com/) server hosts. <br>This is not a tool for normal users, it's designed to be used when hosting a server. <br>Once again, you are responsible for damage made with this tool. <br>Comply with MIT License.
