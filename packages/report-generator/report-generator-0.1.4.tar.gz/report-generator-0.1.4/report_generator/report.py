import datetime as dt
from getpass import getpass
from report_generator.html_tools import banner, color_map
from report_generator.smtp import sendHTMLmailwithattachments, set_credentials, set_password

config_map = {
    'team1': ('Team Name','Sales & Marketing','blue')
}


class Report:
    def __init__(self, team, title):
        assert team in config_map.keys(), f"{team} is not found in config_map"
        self.team = team
        self.title = title
        self.widgets = []

    def add(self,widget,header=""):
        html = f"{widget}<br>"
        if header != "":
            html = f'<h2>{header}</h2>{html}'
        self.widgets.append(html)

    def to_html(self):
        date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        config = config_map[self.team]
        body = "\n".join(self.widgets)
        color = color_map()[config[2]]
        html = banner(date,self.title,config[0],config[1],'',color,body=body)
        return html

    def save(self):
        html = self.to_html()
        with open('test.html','w') as f:
            f.write(html)
    
    def send(self, sender, to):
        body = self.to_html()
        subject = self.title
        sendHTMLmailwithattachments(sender, to, subject, body)

if __name__ == "__main__":
    report = Report('team1',"Fancy report")
    report.add("This is a test","Header of this section")
    report.add("This is another test", "Header of another section")
    sender = 'sender@gmail.com'
    set_password(getpass())
    set_credentials('smtp.gmail.com',sender,sender)
    report.send(sender,[sender])