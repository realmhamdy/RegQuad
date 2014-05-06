import codecs, re, argparse, unittest, os

MSG_FILE = os.path.join(os.path.dirname(__file__), "REGEX_FINAL_EXAMPLE.txt")

firstname_regex = re.compile(r"^Guest Name:\s*(?P<first_name>(?:[\w\.]+))(\s[\w\.]+)?\s*?", re.M)
lastname_regex = re.compile(r"^Guest Name:\s*(?:[\w\.]+)(\s(?P<last_name>[\w\.]+))?\s*?", re.M)
#a phone number can be "Not Provided" or 123-456-7891
phonenumber_regex = re.compile(r"^Phone Number:\s*(?P<phone_number>((?:\w+\s?)|(?:\d+-?))+)\s*?", re.M) 
email_regex = re.compile("^Email Address:\s*(?P<email>.+)\s*?", re.M)
desc_regex = re.compile("^Message From Guest\s*(?P<desc>(?:^.*\s)+?)^.*$(?=\s{2})", re.M)

class RegexTest(unittest.TestCase):
  
  def setUp(self):
    self.txt = codecs.open(MSG_FILE, 'r', encoding="utf-8").read()
    
  def testGuestFirstName(self):
    s1 = "Guest Name: John Hacker"
    match = firstname_regex.search(s1)
    self.assertEqual(match.groupdict()["first_name"], "John", "John didn't match guest")
    s2 = "Guest Name: Mr.John Hacker"
    match = firstname_regex.search(s2)
    self.assertEqual(match.groupdict()["first_name"], "Mr.John", "Mr.John didn't match guest")
    #the real case
    match = firstname_regex.search(self.txt)
    self.assertEqual(match.groupdict()["first_name"], "Hannah", "First name matched '%s'" 
                     % match.groupdict()["first_name"])
    
  def testGuestNameRegex(self):
    s1 = "Guest Name: John Hacker"
    match = lastname_regex.search(s1)
    self.assertEqual(match.groupdict()["last_name"], "Hacker", "Hacker didn't match guest")
    s2 = "Guest Name: Mr.John Hacker"
    match = lastname_regex.search(s2)
    self.assertEqual(match.groupdict()["last_name"], "Hacker", "Hacker didn't match guest")
    #the real case
    match = lastname_regex.search(self.txt)
    self.assertFalse(match.groupdict()["last_name"], "Last name matched '%s'" % match.groupdict()["last_name"])
    
  def testPhoneNumberRegex(self):
    s1 = "Phone Number: 123-45-678"
    match = phonenumber_regex.search(s1)
    self.assertEqual(match.groupdict()["phone_number"], "123", "")
    #real case
    match = phonenumber_regex.search(self.txt)
    self.assertEqual(match.groupdict()["phone_number"].strip(), "Not Provided",
                     "Phone number matched '%s'" % match.groupdict()["phone_number"])
    
  def testEmailRegex(self):
    #real case
    match = email_regex.search(self.txt)
    self.assertEqual(match.groupdict()["email"].strip(), "hannahnimer@yahoo.com", 
                     "Email matched '%s'" % match.groupdict()["email"])
    
  def testDescriptionRegex(self):
    desc = """Message From Guest

How can I respond? rest of line!
Line 2 description!
Simply reply to this email and it will be sent directly to the guest. Alternatively, you may contact the guest at the email address or phone number (if provided) from the guest's contact information above. If you have any additional questions or concerns, please feel free to contact FlipKey.

"""
    match = desc_regex.search(desc)
    self.assertEqual(match.groupdict()["desc"], "How can I respond? rest of line!\nLine 2 description!\n",
                      "Description matched '%s'" % match.groupdict()["desc"])
    #real case
    match = desc_regex.search(self.txt)
    self.assertEqual(match.groupdict()["desc"].strip(), "How can I respond?",
                      "Description matched '%s'" % match.groupdict()["desc"])
    

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--filename",  default=MSG_FILE, help="Name of file that contains text to match against")
  args = parser.parse_args()
  MSG_FILE = args.filename
  unittest.main()