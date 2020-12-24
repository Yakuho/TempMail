from config import function
from base import Mail


class MailPool(Mail):
    def refresh_mail_message(self, *args, **kwargs):
        """
        刷新邮箱消息
        :return:
        """
        result = self.refresh()
        if result:
            print('>> 刷新成功.')
            return True
        else:
            return False

    def refresh_mail_username(self, *args, **kwargs):
        """
        刷新邮箱用户名
        :return:
        """
        result = self.refresh(new_mail=1)
        if result:
            print(f'>> 当前邮箱用户名为: {self.mailbox}{self.rear}')
            return f'{self.mailbox}{self.rear}'
        else:
            return False

    def load_mail_message(self, *args, **kwargs):
        """
        读取邮箱消息
        :return:
        """
        result = self.message()
        if result:
            if self.message_box:
                num = 0
                for item in self.message_box:
                    print(f'>> [{num}] 发送人: {item["from"]}, 发送时间: {item["date"]}, 标题: {item["subject"]}')
                    num += 1
            else:
                print('>> 邮箱消息为空.')
            return self.message_box
        else:
            return False

    def load_mail_detail(self, message_id, *args, **kwargs):
        """
        读取某封邮件的文本
        :param message_id: 邮件的序号
        :param args:
        :param kwargs:
        :return:
        """
        if 0 <= int(message_id) < len(self.message_box):
            result = self.context(self.message_box[int(message_id)]['id'])
        else:
            print('>> 超出范围.')
            return False
        if result:
            print('>>', result)
            return result
        else:
            return False

    def delete_mail_message(self, message_id, *args, **kwargs):
        """
        删除某一条消息
        :param message_id:邮件的序号
        :return:
        """
        if 0 <= int(message_id) < len(self.message_box):
            if self.message_status[int(message_id)]:
                print('>> 已被删除.')
                return False
            else:
                result = self.delete_message(self.message_box[int(message_id)]['id'])
                self.message_status[int(message_id)] = 1
        else:
            print('>> 超出范围.')
            return False
        if result:
            print(f'>> 删除成功.')
            return True
        else:
            return False

    def user(self):
        """
        确定邮箱地址
        :return:
        """
        num = 0
        for i in self.address:
            print(f'[{num}] {self.mailbox}{i}')
            num += 1
        while True:
            try:
                one = int(input('>> 确定你的邮箱地址(序号): '))
                if 0 <= one < len(self.address):
                    self.rear = self.address[one]
                    print(f'>> 当前的邮箱地址为: {self.mailbox}{self.rear}')
                    return f'{self.mailbox}{self.rear}'
                else:
                    print('>> 无效序号!')
            except ValueError:
                print('>> 无效序号!')

    def run(self):
        self.user()
        while True:
            print('\n========================')
            print('1. 刷新当前邮箱消息\n2. 刷新当前邮箱用户名\n3. 读取全部邮箱消息\n'
                  '4. 删除某封邮箱消息\n5. 读取某封邮件详细内容\n6. 重选邮箱地址\n0. 结束')
            print('========================')
            command = input('输入命令: ')
            print()
            func, *args = command.split(' ')
            try:
                eval(function[func])
            except SyntaxError:
                break
            except KeyError:
                print('>> 命令有误.')


if __name__ == '__main__':
    m = MailPool()
    m.run()
