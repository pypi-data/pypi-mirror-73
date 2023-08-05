import aiosqlite

run = 0
Database_dir = ""
item = 0
item2 = 0
item3 = "0"
default_balance = 0
bank = 0
async def get_item(userid):
    """
    Returns an integer from the database"""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        await db.close()
        return item
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def get_item_2(userid):
    """
    Returns an integer from the database"""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        await db.close()
        return item2
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def get_item_3(userid):
    """
    Returns an string from the database"""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item3 = await db.execute("SELECT item3 FROM users WHERE userid = ?", (userid,))
        item3 = await item3.fetchall()
        item3 = item3[0][0]
        await db.close()
        return item3
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def add_item(userid, amount:int):
    """
    Adds items to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        item += amount
        await db.execute("UPDATE users SET item = ? WHERE userid = ?", (item, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_item(userid, amount:int):
    """
    Removes items to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        item = item - amount
        await db.execute("UPDATE users SET item = ? WHERE userid = ?", (item, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_item(userid, amount:int):
    """
    Sets items to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item = await db.execute("SELECT item FROM users WHERE userid = ?", (userid,))
        item = await item.fetchall()
        item = item[0][0]
        item = amount
        await db.execute("UPDATE users SET item = ? WHERE userid = ?", (item, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def add_item_2(userid, amount:int):
    """
    Adds item2 to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        item2 += amount
        await db.execute("UPDATE users SET item2 = ? WHERE userid = ?", (item2, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_item_2(userid, amount:int):
    """
    Removes item2 from the by the amount database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        item2 = item2 - amount
        await db.execute("UPDATE users SET item2 = ? WHERE userid = ?", (item2, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_item_2(userid, amount:int):
    """
    Set item2 to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item2 = await db.execute("SELECT item2 FROM users WHERE userid = ?", (userid,))
        item2 = await item2.fetchall()
        item2 = item2[0][0]
        item2 = amount
        await db.execute("UPDATE users SET item2 = ? WHERE userid = ?", (item2, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_item_3(userid, amount:int):
    """
    Adds item3 to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item3 = await db.execute("SELECT item3 FROM users WHERE userid = ?", (userid,))
        item3 = await item3.fetchall()
        item3 = item3[0][0]
        item3 += amount
        await db.execute("UPDATE users SET item3 = ? WHERE userid = ?", (item3, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_item_3(userid, amount:int):
    """
    Remove item3 from the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item3 = await db.execute("SELECT item3 FROM users WHERE userid = ?", (userid,))
        item3 = await item3.fetchall()
        item3 = item3[0][0]
        item3 = item3 - amount
        await db.execute("UPDATE users SET item3 = ? WHERE userid = ?", (item3, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_item_3(userid, amount:int):
    """
    Set item3 to the database."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        item3 = await db.execute("SELECT item3 FROM users WHERE userid = ?", (userid,))
        item3 = await item3.fetchall()
        item3 = item3[0][0]
        item3 = amount
        await db.execute("UPDATE users SET item3 = ? WHERE userid = ?", (item3, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def get_bank(userid):
    """
    Returns the bank balance of the userid provided."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute("SELECT bank FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        await db.close()
        return bank
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_bank(userid, amount:int):
    """
    Adds balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute("SELECT bank FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        bank += amount
        await db.execute("UPDATE users SET bank = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_bank(userid, amount:int):
    """
    Remove from the bank balance from the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = await db.execute("SELECT bank FROM users WHERE userid = ?", (userid,))
        bank = await bank.fetchall()
        bank = bank[0][0]
        bank = bank - amount
        await db.execute("UPDATE users SET bank = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def get_balance(userid):
    """
    Returns the balance of the userid provided."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        await db.close()
        return balance
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_balance(userid, amount:int):
    """
    Adds balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        balance += amount
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (balance, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def remove_balance(userid, amount:int):
    """
    Remove balance from the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = await db.execute("SELECT balance FROM users WHERE userid = ?", (userid,))
        balance = await balance.fetchall()
        balance = balance[0][0]
        balance = balance - amount
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (balance, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def add_user(userid):
    """
    Adds user to the database with the default values."""
    try:
        global item, item2, item3, default_balance, bank
        db = await aiosqlite.connect(Database_dir + "main.db")
        await db.execute("INSERT INTO users(balance,bank,userid,item,item2,item3) VALUES(?,?,?,?,?,?)", (default_balance, bank, userid,item,item2, item3))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_balance(userid, amount):
    """
    Sets choosen balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        balance = amount
        await db.execute("UPDATE users SET balance = ? WHERE userid = ?", (balance, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass

async def set_bank(userid, amount):
    """
    Sets choosen balance to the userid."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        bank = amount
        await db.execute("UPDATE users SET bank = ? WHERE userid = ?", (bank, userid))
        await db.commit()
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def basic_user_check(userid):
    "Checks if user is in database returns a boolean."
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        user = await db.execute("SELECT userid FROM users WHERE userid = ?", (userid,))
        user = await user.fetchall()
        await db.close()
        if not user:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def user_check(userid):
    """
    Checks if user is in the database and if not adds him by the default values."""
    try:
        db = await aiosqlite.connect(Database_dir + "main.db")
        user = await db.execute("SELECT userid FROM users WHERE userid = ?", (userid,))
        user = await user.fetchall()
        if not user:
            await db.execute("INSERT INTO users(balance,bank,userid,item,item2,item3) VALUES(?,?,?,?,?,?)", (default_balance, bank, userid,item,item2, item3))
            await db.commit()
        else:
            pass
        await db.close()
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass
async def setup_database(dir):
    """
    Creates the db file and the table in your chosen directory."""
    try:
        global run
        if run == 0:
            run = 1
            db = await aiosqlite.connect(dir + "main.db")
            await db.execute("CREATE TABLE users(balance INTEGER, bank INTEGER, userid INTEGER, item INTEGER, item2 INTEGER, item3 TEXT)")
            await db.commit()
            await db.close()
    except Exception as e:
        try:
            await db.close()
        except:
            pass
    except Exception as e:
        print(e)
        try:
            await db.close()
        except:
            pass



