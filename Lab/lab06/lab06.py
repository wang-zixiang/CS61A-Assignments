class Transaction:
    def __init__(self, id, before, after):
        self.id = id
        self.before = before
        self.after = after

    def changed(self):
        """Return whether the transaction resulted in a changed balance."""
        "*** YOUR CODE HERE ***"
        return self.before != self.after

    def report(self):
        """Return a string describing the transaction.

        >>> Transaction(3, 20, 10).report()
        '3: decreased 20->10'
        >>> Transaction(4, 20, 50).report()
        '4: increased 20->50'
        >>> Transaction(5, 50, 50).report()
        '5: no change'
        """
        msg = 'no change'
        if self.changed():
            "*** YOUR CODE HERE ***"
            if self.after > self.before:
                verb = "increased"
            else:
                verb = "decreased" 
            msg = verb + " " + str(self.before) + "->" +str(self.after)
        return str(self.id) + ': ' + msg

class BankAccount:
    """A bank account that tracks its transaction history.

    >>> a = BankAccount('Eric')
    >>> a.deposit(100)    # Transaction 0 for a
    100
    >>> b = BankAccount('Erica')
    >>> a.withdraw(30)    # Transaction 1 for a
    70
    >>> a.deposit(10)     # Transaction 2 for a
    80
    >>> b.deposit(50)     # Transaction 0 for b
    50
    >>> b.withdraw(10)    # Transaction 1 for b
    40
    >>> a.withdraw(100)   # Transaction 3 for a
    'Insufficient funds'
    >>> len(a.transactions)
    4
    >>> len([t for t in a.transactions if t.changed()])
    3
    >>> for t in a.transactions:
    ...     print(t.report())
    0: increased 0->100
    1: decreased 100->70
    2: increased 70->80
    3: no change
    >>> b.withdraw(100)   # Transaction 2 for b
    'Insufficient funds'
    >>> b.withdraw(30)    # Transaction 3 for b
    10
    >>> for t in b.transactions:
    ...     print(t.report())
    0: increased 0->50
    1: decreased 50->40
    2: no change
    3: decreased 40->10
    """

    # *** YOU NEED TO MAKE CHANGES IN SEVERAL PLACES IN THIS CLASS ***

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
        self.transactions = []
        self.id_counters = 0

    def deposit(self, amount):
        """Increase the account balance by amount, add the deposit
        to the transaction history, and return the new balance.
        """
        a = Transaction(self.id_counters, self.balance, self.balance + amount)
        self.balance = self.balance + amount
        self.transactions.append(a)
        self.id_counters += 1
        return self.balance

    def withdraw(self, amount):
        """Decrease the account balance by amount, add the withdraw
        to the transaction history, and return the new balance.
        """
        
        if amount > self.balance:
            a = Transaction(self.id_counters, self.balance, self.balance)
            self.transactions.append(a)
            self.id_counters += 1
            return 'Insufficient funds'
        a = Transaction(self.id_counters, self.balance, self.balance - amount)
        self.balance = self.balance - amount
        self.transactions.append(a)
        self.id_counters += 1
        return self.balance


class Email:
    """An email has the following instance attributes:

        msg (str): the contents of the message
        sender (Client): the client that sent the email
        recipient_name (str): the name of the recipient (another client)
    """
    def __init__(self, msg, sender, recipient_name):
        self.msg = msg
        self.sender = sender
        self.recipient_name = recipient_name

class Server:
    """Each Server has one instance attribute called clients that is a
    dictionary from client names to client objects.
    """
    def __init__(self):
        self.clients = {}

    def send(self, email):
        """Append the email to the inbox of the client it is addressed to.
            email is an instance of the Email class.
        """
        recipient = self.clients[email.recipient_name] 
        recipient.inbox.append(email)

    def register_client(self, client):
        """Add a client to the clients mapping (which is a 
        dictionary from client names to client instances).
            client is an instance of the Client class.
        """
        self.clients[client.name] = client

class Client:
    """A client has a server, a name (str), and an inbox (list).

    >>> s = Server()
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> a.compose('Hello, World!', 'Bob')
    >>> b.inbox[0].msg
    'Hello, World!'
    >>> a.compose('CS 61A Rocks!', 'Bob')
    >>> len(b.inbox)
    2
    >>> b.inbox[1].msg #msg是Email的一个instance，所以有.sender,而msg.sender是一个Client类
    'CS 61A Rocks!'
    >>> b.inbox[1].sender.name
    'Alice'
    """
    def __init__(self, server, name):# server是Server类的一个实例，所以在初始化Client的时候要对server.register,相当于注册一个账号。
        self.inbox = []
        self.server = server
        self.name = name
        # server.register_client(name) 这个是错的
        server.register_client(self) #如果不挂载到serve上就无法收消息

    def compose(self, message, recipient_name):
        """Send an email with the given message to the recipient."""
        email = Email(message, self, recipient_name)
        self.server.send(email)


class Mint:
    """A mint creates coins by stamping on years.

    The update method sets the mint's stamp to Mint.present_year.

    >>> mint = Mint() #mint是一个实例，他是一个铸币厂
    >>> mint.year #可以查看当前年份
    2024
    >>> dime = mint.create(Dime) #调用mint的一个方法creat去铸币
    >>> dime.year # ***Q1***： dime是一个Coin类，所以有year属性，但是这个year什么时候传入的?
    2024
    >>> Mint.present_year = 2104  # Time passes #***Q2***:这个present_year又没有写在初始化__init__里面,为啥可以用点方法调用？
    >>> nickel = mint.create(Nickel) #铸造了一个5分硬币
    >>> nickel.year     # The mint has not updated its stamp yet #查看这个硬币时间，但是这个时间是mint.year,而不是present_time
    2024
    >>> nickel.worth()  # 5 cents + (80 - 50 years) #查看面值
    35
    >>> mint.update()   # The mint's year is updated to 2104 #更新mint的时间
    >>> Mint.present_year = 2179     # More time passes #?为啥这个present_time还变化了?这个不是一个固定值么,写在mint类里面的？
    >>> mint.create(Dime).worth()    # 10 cents + (75 - 50 years)
    35
    >>> Mint().create(Dime).worth()  # A new mint has the current year 这是啥意思，直接把Dime类给传进去了？
    10
    >>> dime.worth()     # 10 cents + (155 - 50 years)
    115
    >>> Dime.cents = 20  # Upgrade all dimes! 更行了10分的价格
    >>> dime.worth()     # 20 cents + (155 - 50 years)
    125
    """
    present_year = 2024

    def __init__(self):
        self.update()

    def create(self, coin):#Coin是一个类，第二个值会是Nickel或者Dime
        "*** YOUR CODE HERE ***"
        return coin(self.year)
        

    def update(self):
        "*** YOUR CODE HERE ***"
        self.year = Mint.present_year #为什么这里不能调用呢present_year看起来应该是这个类里面的类全局变量吧？

class Coin:
    cents = None # will be provided by subclasses, but not by Coin itself

    def __init__(self, year):
        self.year = year

    def worth(self):
        "*** YOUR CODE HERE ***"#这里我要计算worth需要用到present_year，但是他没传进来怎么办？
        add_worth = Mint.present_year - self.year - 50
        return self.cents + max(0,add_worth)


class Nickel(Coin):
    cents = 5

class Dime(Coin):
    cents = 10

