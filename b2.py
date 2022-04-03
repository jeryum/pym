import sys,os,time
def j(z):
        for e in z + '\n':
                sys.stdout.write(e)
                sys.stdout.flush()
                time.sleep(0.07)

os.system("figlet 'bwc'")    
print("-created by jerome")               
     
a = """ 
\033[31mhello
there
how you doing?"""

b = "\033[92mwant to make bday web for your hoes?"

j(a)
print(" ")
time.sleep(1)
j(b)
time.sleep(1)
print("\033[33mno just kidding")
time.sleep(1)

con = input("\033[92mname of person have bday? :")
img = input("path of image? :")
age = input("age of the person ? :")
m = input("month ? :")
y = input("year ? :")
d =  input("day? :")
mes = input("message for the person? :")




##########source code
c1 =  """<!DOCTYPE html>
<html lang="en">
<head>
				<meta charset="UTF-8">
				<title>Happy birthday """
c2 = con
c3 = """</title>
				<script src="https://kit.fontawesome.com/dee585cdde.js" crossorigin="anonymous"></script>
				<link rel="preconnect"
				 href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Display:ital,wght@1,200;1,300&display=swap" rel="stylesheet">
							
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
	<style>
			body{
					background-color:#bfeaff;
			}		
			*{
							font-family: 'Noto Sans Display', sans-serif;
			}
			#a{
				font-size:25px;
			}
			
			#b{
			 overflow-x:hidden;
			 width:230px;
		
			 border: 6px double white;
			}
			.hag {

            position: absolute;

            top: 17%;

            left: 50%;

            transform: translate(-50%, -50%);

        }
		#c{
			font-size: 60px;
			font-family: 'Noto Sans Display', sans-serif;

            color: transparent;

            text-align: center;

            animation: effect 2s linear infinite;
			
					\
		}
		
		@keyframes effect {

            0% {

                background: linear-gradient(

                       blue , red);
                        

                -webkit-background-clip: text;

            }
 

            100% {

                background: linear-gradient(

                        #3CE7D7, #000FFF);

                -webkit-background-clip: text;

            }

        }
			#d{
						color:#000000;	
				font-size:30px;
				
			}
					</style>
			"""
c4 = """<br>
					<center>
		<p id="a">Happy """
c5 = age
ctite =  """  birthday
 </p>
	<div class="hag">
		<h2 id="c"> """
c6 = con  
c7 = """</h2>
		</div>
		<br>
		<br>
		<img src=" """
c8 = img 
c9 = """" id="b">
	<p id="c" style="font-size:20px;">message : <br> """
c10 = mes

c11 = """</p>
		<br>
	<br><br>
	<p id="d">"""
cs = """<center><fa-2x i class="fa-3x fa-solid fa-cake-candles"></i></center>"""
hahak = """<p style="position:absolute;">-created by jerome</p>"""
c12 = m
c13 = d
c14 = y
c15 = """</p>
		</center>
</body>
</html>
"""
choice = input("\033[1;36;40m[+] Do You Want To Continue [y/n] : ")
if choice == "y":
	time.sleep(2)
	os.system('clear')
	print(" ")
	j("making your page")
	fo = open("bday.html","w")
    
 
elif choice == "n":
	exit()

fo.write(c1)
fo.write(c2)
fo.write(c3)
fo.write(c4)
fo.write(ctite)
fo.write(c6)
fo.write(c7)
fo.write(c8)
fo.write(c9)
fo.write(c10)
fo.write(cs)
fo.write(hahak)
fo.write(c11)

fo.write(c12)
fo.write(" ")
fo.write(c13)
fo.write(" ")
fo.write(c14)
fo.write(" ")
fo.write(c15)

print(" ")
print ("""file save as bday.html.

""")

fo.close()
