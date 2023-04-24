from DetectMask import MaskDetection
from Main import Main

if __name__ == "__main__":
    M = MaskDetection()
    m = Main()
    """Main Program For Project"""
    print("Operations:")
    print("1. Start Program.")
    print("2. Login.")
    print("3. Setup.")
    choice = int(input("Your Choice: "))
    if choice == 1:
        M.Start()
    elif choice == 2:
        m.Login()
    elif choice == 3:
        m.Setup()
    else:
        input("wrong choice! \nPress any key to continue.....")
    del M
    del m
