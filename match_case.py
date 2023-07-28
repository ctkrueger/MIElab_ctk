#match case requires python >= 3.10 to work
color = input("whats your fav color:\n")

match color:
    case "red":
        print("Red is basic af wtf")
    case "yellow":
        print("Okay hufflepuff")
    case "green":
        print("respectable")
    case "orange":
        print("me too")
    case _ :
        print("literally not even a main character color")