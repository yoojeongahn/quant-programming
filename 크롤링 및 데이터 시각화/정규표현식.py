## 정규표현식
import re
data = '동 기업의 매출액은 전년 대비 29.2% 늘어났습니다.'
# re.findall('\d+.\d+%', data)

'''
| \d | 숫자와 매치, [0-9]와 동일한 표현식 |
| \D | 숫자가 아닌 것 매치, [^0-9]와 동일한 표현식 |
| \s | whitespace(공백) 문자와 매치, [ \t\n\r\f\v]와 동일한 표현식 |
| \S | whitespace 문자가 아닌 것과 매치, [^\t\n\r\f\v]와 동일한 표현식 |
| \w | 문자+숫자(alphanumeric)와 매치, [a-zA-Z0-9]와 동일한 표현식 |
| \W | 문자+숫자(alphanumeric)가 아닌 문자와 매치, [^a-zA-Z0-9]와 동일한 표현식 |

. : 모든 문자   a[.]c
* : 반복문      ca*t
+ : 최소 1번 이상 반복
{} : 반복 횟수 고정
? : {0, 1}

match(): 시작부분부터 일치하는 패턴을 찾는다.
search(): 첫 번째 일치하는 패턴을 찾는다.
findall(): 일치하는 모든 패턴을 찾는다.
finditer(): findall()과 동일하지만 그 결과로 반복 가능한 객체를 반환한다.
'''

p = re.compile('[a-z]+')
m = p.match('python')   # print(m.group()) -> 'python'
m = p.match('Use python') #print(m) -> None

m = p.search('Use python')  # print(m) -> match='se'

p = re.compile('[a-zA-Z]+')
m = p.findall('Life is too short, You need Python.')
# print(m)  ->  ['Life', 'is', 'too', 'short', 'You', 'need', 'Python']

# 정규표현식 연습
num = """r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t15\n\r\n\t\t\t\t\t\t\t
        \t23\r\n\t\t\t\t\t\t\t\t29\r\n\t\t\t\t\t\t\t\t34\r\n\t\t\t\t\t
        \t\t\t40\r\n\t\t\t\t\t\t\t\t44\r\n\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t"""
p = re.compile('[0-9]+')
m = p.findall(num)  # print(m) ->   ['15', '23', '29', '34', '40', '44']


dt = '> 오늘의 날짜는 2022.12.31 입니다.'
p = re.compile('[0-9]+.[0-9]+.[0-9]+')
m = p.findall(dt)   # print(''.join(m))  ->  2022.12.31