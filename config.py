from requests.exceptions import Timeout
function = {
    '1': 'self.refresh_mail_message(*args)',
    '2': 'self.refresh_mail_username(*args)',
    '3': 'self.load_mail_message(*args)',
    '4': 'self.delete_mail_message(*args)',
    '5': 'self.load_mail_detail(*args)',
    '6': 'self.user(*args)',
    '0': 'break'
}
timeout = 10


def autoRetry(func):
    def retry(*args, **kwargs):
        errorTime = 8
        for i in range(errorTime):
            try:
                response = func(*args, **kwargs)
                if response:
                    return response
            except Timeout:
                pass
            print(f'访问失败{i + 1}次')
        else:
            print(f'访问失败超过{errorTime}次, 超时')
            return False
    return retry

