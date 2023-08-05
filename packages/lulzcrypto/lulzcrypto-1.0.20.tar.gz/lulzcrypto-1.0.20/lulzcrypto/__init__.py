# -*- coding: utf-8 -*-
#
#  Simple encryptor.
#  Created by LulzLoL231 at 02/07/20
#
import requests
import jwt

import lulzcode


class CryptoError(Exception):
    pass


class PastebinError(CryptoError):
    pass


class Crypto:
    def __init__(self, key: str, pastebin_api: str=None):
        self.PASTEBIN_API_ENDPOINT = 'https://pastebin.com/api/api_post.php'
        self.key = key
        self.pastebin_key = pastebin_api


    def _UploadToPastebin(self, text: str) -> str:
        '''Create paste on pastebin with text in it.
        
        Args:
            `text`: sometext for paste.
        
        Returns:
            string with URL to pastebin paste.
        
        Raises:
            `PastebinError` for any API error.'''
        data = {
                'api_dev_key': self.pastebin_key,
                'api_option': 'paste',
                'api_paste_code': text,
                'api_paste_private': 2
                }
        resp = requests.post(self.PASTEBIN_API_ENDPOINT, data)
        if 'Bad API request' in resp.text:
            raise PastebinError(resp.text)
        else:
            return resp.text
    
    def _EncodeInLulzCode(self, text: str) -> str:
        '''Encode provided text with LulzCode.
        
        Args:
            `text`: sometext for encoding.
        
        Returns:
            string with encoded text.'''
        return lulzcode.encode(text)
    
    def _EncryptWithJWT(self, text: str) -> str:
        '''Encrypt provided text with JWT.
        
        Args:
            `text`: sometext for encrypting.
        
        Returns:
            string with encrypted text.'''
        return jwt.encode({'payload': text}, self.key).decode()
    
    def _DecodeFromLulzCode(self, text: str) -> str:
        '''Decode text from LulzCode.
        
        Args:
            `text`: encoded in LulzCode text
        
        Returns:
            string with cleartext'''
        return lulzcode.decode(text)

    def _DecryptWithJWT(self, text: str) -> str:
        '''Decrypt encrypted with JWT text.
        
        Args:
            `text`: encrypted text.
        
        Returns:
            string with cleartext.'''
        return jwt.decode(text, self.key)['payload']
    
    def encrypt(self, text: str, upload: bool=True) -> str:
        '''Encrypt cleartext and upload it to pastebin.com, if provided API key.
        
        Args:
            `text`: some text.
            `upload`: upload to pastebin.com or not?
        
        Returns:
            string with URL to pastebin.com paste or just encrypted text.

        Info:
            if upload is `True`, but pastebin API key is not provided, just return encrypted text.'''
        fr = self._EncryptWithJWT(text)
        sr = self._EncodeInLulzCode(fr)
        if upload:
            if self.pastebin_key:
                result = self._UploadToPastebin(sr)
            else:
                result = sr
        else:
            result = sr
        return result
    
    def decrypt(self, text: str=None, pastebin: str=None) -> str:
        '''Decrypt provided text, or upload it and decrypt it.
        
        Args:
            `text`: encrypted with LulzCrypto text.
            `pastebin`: pastebin.com paste URL or pasteID.
        
        Returns:
            string with decrypted text.'''
        if (text is None) and (pastebin is None):
            raise CryptoError('Please, give "text" var or "pastebin".')
        else:
            if text:
                fr = self._DecodeFromLulzCode(text)
                sr = self._DecryptWithJWT(fr)
                return sr
            if pastebin:
                if 'https://pastebin.com' not in pastebin:
                    pastebin = 'https://pastebin.com/raw/' + pastebin
                else:
                    if 'raw' not in pastebin:
                        pastebin = 'https://pastebin.com/raw/' + pastebin.split('/')[3]
                resp = requests.get(pastebin)
                if resp.status_code == 404:
                    raise PastebinError('Paste not found.')
                elif '<!DOCTYPE HTML>' in resp.text:
                    raise PastebinError('Unknown error.')
                else:
                    fr = self._DecodeFromLulzCode(resp.text)
                    sr = self._DecryptWithJWT(fr)
                    return sr
