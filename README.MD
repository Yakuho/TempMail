# 临时邮箱接口

API:

- refresh_mail_message: 刷新邮件消息
- refresh_mail_username: 刷新邮件用户名(如******@163.com, ****就是用户名)
- load_mail_message: 读取邮件消息(如详细消息对应的id、time、sender等)
- load_mail_detail: 读取某封邮件的文本(要先读取邮件消息，然后在self.message_box
里面根据索引读取对应的文本；或者也可以改成根据消息的id进行读取)
- delete_mail_message: 与读取邮件的文本用法一致
- user: 确定邮件地址(如******@163.com, 163.com就是地址)