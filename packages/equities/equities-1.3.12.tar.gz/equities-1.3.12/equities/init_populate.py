

from objects import Universe,Company

if __name__=='__main__':

    u = Universe()

    quarters = ["2019q2","2019q3","2019q4","2020q1"]
    u.download(quarters=quarters)
    
