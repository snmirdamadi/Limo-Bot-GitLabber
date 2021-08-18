import asyncio
import re


import gitlab

from limoo import LimooDriver


async def respond(event):
    if (event['event'] == 'message_created'
            and not (event['data']['message']['type']
                     or event['data']['message']['user_id'] == self['id'])):
        message_id = event['data']['message']['id']
        try:
            pattern = '/گیتلب'
            token = re.sub(pattern, '', event['data']['message']['text']).strip()
            gl = gitlab.Gitlab('http://gitlab.com/', private_token=token)
            data = ''
            for project in gl.projects.list(owned=True):
                data += project.attributes['name'] + '\n'
        except Exception as e:
            print(e)
            data = 'اطلاعات نادرست است'
        finally:
            event['data']['message']['text'] = data
            thread_root_id = event['data']['message']['thread_root_id']
            direct_reply_message_id = event['data']['message']['thread_root_id'] and event['data']['message']['id']
            response = await ld.messages.create(
                event['data']['workspace_id'],
                event['data']['message']['conversation_id'],
                event['data']['message']['text'],
                thread_root_id=thread_root_id or message_id,
                direct_reply_message_id=thread_root_id and message_id)




async def main():
    global ld, self
    ld = LimooDriver('web.limoo.im', 'affir-bot', 'wvqxr0n17ivok1zo3spk')
    try:
        self = await ld.users.get()
        forever = asyncio.get_running_loop().create_future()
        ld.set_event_handler(lambda event: asyncio.create_task(respond(event)))
        await forever
    finally:
        await ld.close()




if __name__ == '__main__':
    asyncio.run(main())
