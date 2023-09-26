import unittest
from unittest.mock import Mock
from Discord_bot_python import on_message

class TestOnMessage(unittest.TestCase):
    def setUp(self):
        self.message = Mock()
    
    def test_On_message_0793b7ef2f(self):
        # Test case 1: message from the bot itself
        self.message.author = "Cheatbot"
        self.message.content = "hello"
        self.assertIsNone(on_message(self.message))

        # Test case 2: message starts with "hello" or "Hello"
        self.message.author = "user"
        self.message.content = "hello"
        self.message.channel.send.assert_called_with("Hello, I am Cheatbot, here to help you cheat!")

        # Test case 3: message starts with "cheat ping"
        self.message.content = "cheat ping"
        self.message.channel.send.assert_called_with(f'{round(client.latency*1000)}ms')

        # Test case 4: message starts with "cheat wiki"
        self.message.content = "cheat wiki Python"
        self.message.channel.send.assert_called()
        
        # Test case 5: message starts with "cheat question"
        self.message.content = "cheat question What is Python? 4"
        self.message.channel.send.assert_called()

        # Test case 6: message starts with "cheat help"
        self.message.content = "cheat help"
        self.message.channel.send.assert_called()

        # Test case 7: message starts with "cheat error"
        self.message.content = "cheat error SIGSEV"
        self.message.channel.send.assert_called()

if __name__ == '__main__':
    unittest.main()
