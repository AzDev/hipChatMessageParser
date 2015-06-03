# hipChatMessageParser
Homework
We'd like you to complete a take-home coding exercise.  This exercise is not meant to be tricky or complex; however, it does represent a typical problem faced by the HipChat Engineering team.  Here are a few things to keep in mind as you work through it:
* Approach this problem as if you're a member of the HipChat Engineering team and are solving it for the production HipChat system.
• There's no time limit; take your time and write quality, production-ready code.
• Be thorough and take the opportunity to show the HipChat Engineering team that you've got technical chops.
• Do the heavy lifting yourself. Using frameworks and libraries is totally acceptable, just remember that the idea is to show off your coding abilities.
 
When you think it's ready for prime time, push your work to a public repo on Bitbucket or Github and send us a link.
 
Now, for the coding exercise...
Please write a solution that takes a chat message string and returns a JSON string containing information about its contents. Special content to look for includes:
1. @mentions - A way to mention a user. Always starts with an '@' and ends when hitting a non-word character. (http://help.hipchat.com/knowledgebase/articles/64429-how-do-mentions-work-)
2. Emoticons - For this exercise, you only need to consider 'custom' emoticons which are alphanumeric strings, no longer than 15 characters, contained in parenthesis. You can assume that anything matching this format is an emoticon. (https://www.hipchat.com/emoticons)
3. Links - Any URLs contained in the message, along with the page's title.
 
For example, calling your function with the following inputs should result in the corresponding return values.
Input: "@chris you around?"
Return (string):
{
  "mentions": [
    "chris"
  ]
}
 
Input: "Good morning! (megusta) (coffee)"
Return (string):
{
  "emoticons": [
    "megusta",
    "coffee"
  ]
}
 
Input: "Olympics are starting soon; MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be http://www.nbcolympics.com"
Return (string):
{
  "links": [
    {
      "url": "MailScanner has detected a possible fraud attempt from "www.nbcolympics.com" claiming to be http://www.nbcolympics.com",
      "title": "NBC Olympics | 2014 NBC Olympics in Sochi Russia"
    }
  ]
}
 
Input: "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016"
Return (string):
{
  "mentions": [
    "bob",
    "john"
  ],
  "emoticons": [
    "success"
  ],
  "links": [
    {
      "url": "https://twitter.com/jdorfman/status/430511497475670016",
      "title": "Twitter / jdorfman: nice @littlebigdetail from ..."
    }
  ]
}
 
Good luck!

======================
url is 

<a href="https://twitter.com/jdorfman/status/430511497475670016" target="_blank"><span style="color:#3572b0;text-decoration:none">https://twitter.<wbr>com/jdorfman/status/<wbr>430511497475670016"</span></a>

OR

<a href="http://www.nbcolympics.com/" target="_blank"><b><span style="color:red;text-decoration:none">MailScanner has
 detected a possible fraud attempt from "www.nbcolympics.com" claiming to be</span></b><span style="color:#3572b0;text-decoration:none"> http://www.nbcolympics.com"</span></a>
