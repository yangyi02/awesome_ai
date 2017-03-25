import re

lines = open('ai_giants.html').readlines()

data = []
for line in lines:
   if line.startswith('\t<blockquote>'):
      pattern = re.findall(r'<blockquote><p style="text-align:left"><a href="(.*)">(.*)<\/a><span style="float:right">(.*)<\/span><\/p></blockquote>', line)
      data.append([pattern[0][0], pattern[0][1], pattern[0][2]])

with open('ai_giants.md', 'w') as handle:
   for item in data:
      str = '- [' + item[1] + '](' + item[0] + ') ' + item[2] + '\n'
      handle.write(str)

