import re
import urllib2

template_lines = open('template.html').readlines()

lines = open('README.md').readlines()

data = []
for line in lines:
   if line.startswith('-'):
      pattern = re.findall(r'- \[(.*)\]\((.*)\) (.*)', line)
      print(pattern)
      print('testing url: %s' % pattern[0][1])
      try:
         urllib2.urlopen(pattern[0][1])
      except urllib2.HTTPError:
         pass
      data.append([pattern[0][0], pattern[0][1], pattern[0][2]])

with open('ai_giants.html', 'w') as handle:
   for line in template_lines[:-1]:
      handle.write(line)
   for item in data:
      str = '\t<blockquote><p style="text-align:left"><a href="%s">%s</a><span style="float:right">%s</span></p></blockquote>\n' \
            % (item[1], item[0], item[2])
      handle.write(str)
   handle.write(template_lines[-1])
