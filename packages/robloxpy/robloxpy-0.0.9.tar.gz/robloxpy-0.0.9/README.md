# RobloxPyOfficial
 RobloxPy is a python API wrapper for the roblox web api's. This allows for quick and easy integration of these API's into a python project.
 
 ## Table of Contents


* [Getting Started](#Getting-Started)
  * [Prerequisites](#Prerequisites)
  * [Installation](#Installation)
* [Usage](#Usage)
  * [Current Features](#Features)
  * [Usage Examples](#Examples)
    * [External Functions](#External-Functions)
        * [User Functions](#User-Functions)
            * [LimitedRelated](#Limited-Functions)
        * [Group Functions](#Group-Functions)
        * [Asset Functions](#Asset-Functions)
    * [Internal Functions](#Internal-Functions)
        * [User Functions](#Internal-User-Functions)
        * [Group Functions](#Internal-Group-Functions)

# Getting-Started
To use the wrapper you will need to download and import robloxpy into your current project. The project has not external requirements that is not included within the defaults of a python install.

## Prerequisites
N/A

## Installation
Before you can import robloxpy you will first need to install it through pip
```python
pip install robloxpy
```

If you wish to update robloxpy in the future you can also do this through pip
```python
pip install robloxpy --upgrade
```

# Usage
This section will cover what is currently supported by the API and how they can be used

# Features
* External
    * User
        * NameToID(UserName) 
        * GetName(UserID)
        * IsOnline(UserID)
        * GetFriends(UserID)
        * GetOnlineFriends(UserID)
        * GetOfflineFriends(UserID)
        * GetUserGroups(UserID)
    * RAP
        * GetUserRap(UserID)
        * GetUserLimitedValue(UserID)
        * GetUserNoDemandLimiteds(UserID)
        * GetUserLowDemandLimiteds(UserID)
        * GetUserNormalDemandLimiteds(UserID)
        * GetUserGoodDemandLimiteds(UserID)
        * GetUserTerribleDemandLimiteds(UserID)
    * Group
        * IsGroupOwned(GroupID)
        * GetGroupName(GroupID)
        * GetGroupDescription(GroupID)
        * GetGroupShout(GroupID)
        * IsGroupOpen(GroupID)
        * GetGroupMembers(GroupID)
        * GetGroupAllies(GroupID)
        * GetGroupEnemies(GroupID)
    * Assets
        * CanManage(UserID,GroupID)

* Internal
    * User
        * GetUserID(Cookie)
        * GetUserName(Cookie)
        * GetEmail(Cookie)
        * IsEmailVerified(Cookie)
        * CanTrade(Cookie)
        * IsOver13(Cookie)
        * IsTwoStepEnabled(Cookie)
        * IsAccountPinEnabled(Cookie)
        * GetRobux(Cookie)
        * IsPremium(Cookie)
        * GetAvatar(Cookie)
        * IsFollowing(Cookie, UserID)
        * FollowUser(Cookie, UserID)
        * UnfollowUser(Cookie, UserID)
        * BlockUser(Cookie, UserID)
        * UnblockUser(Cookie, UserID)
        * SendFriendRequest(Cookie,UserID)
        * Unfriend(Cookie,UserID)
        * TotalFriends(Cookie)
    * Group
        * ClaimGroup(Cookie,GroupID)
        * JoinGroup(Cookie,GroupID)
        * LeaveGroup(Cookie,GroupID)
        * GetFunds(Cookie,GroupID)
        * PayGroupFunds(Cookie,GroupID,UserID,RobuxAmount)
        * PayGroupPercentage(Cookie,GroupID,UserID,Percentage)
        * PostGroupWall(Cookie,GroupID,Text)

# Examples
Below are examples of how to use each of the functions within robloxpy
# External-Functions
These functions do not require any cookies can be used without any data, these are limited to GET based on what roblox provides
* ## User-Functions
These functions allow you to get data in regards to a specific user through the use of their UserID or UserName

* NameToID(UserName) 
```python
robloxpy.NameToID(kristan99) #Get the UserID of the roblox user with the name kristan99
Output > 1368140
```

* GetName(UserID)
```python
robloxpy.GetName(1368140) #Get the name of the roblox user with the ID of 1368140
Output > kristan99
```

* IsOnline(UserID)
```python
robloxpy.IsOnline(1368140) #Check if the user with the ID 1368140 is online
Output > False
```

* GetFriends(UserID)
```python
robloxpy.GetFriends(1368140) #Return a list of all friends of the roblox user with the ID 1368140
Output > ['SlimemingPlayz', 'E_xitium', 'Kawaii_Katicorn99', 'KatieeLouisee99', 'Yung_nignogpaddywog', 'BigDDave', 'Nosowl', 'Mirro_rs', 'Gareth1990', 'Voxxes', 'matantheman', 'ItzDishan', 'Xulfite', 'CinnabonNinja', 'hotrod56478', 'roxo_pl', 'VIPOrder', 'GlowwLikeThat', 'BritishP0litics', 'Nicolas9970', 'YunPlant', 'sirjoshh', 'iMistifye', 'Scorp1x', 'Fribbzdaman', 'xMcKenziee', 'AjinKovac', 'Angels_Develop', 'RonerRehnskiold', 'Natty32', 'agnen', 'yusufrad22', 'RocketValkyrie', 'methanshacked', 'GingyWyven', 'KingsmanSS', 'glitch19']
```
* GetOnlineFriends(UserID)
```python
robloxpy.GetOnlineFriends(1368140) #Get a list of online friends of the roblox user with the ID 1368140
Output > ['Mirro_rs', 'Natty32']
```

* GetOfflineFriends(UserID) 
```python
robloxpy.GetOfflineFriends(1368140) #Get a list of offline friends of the roblox user with the ID 1368140
Output > ['SlimemingPlayz', 'E_xitium', 'Kawaii_Katicorn99', 'KatieeLouisee99', 'Yung_nignogpaddywog', 'BigDDave', 'Nosowl', 'Gareth1990', 'Voxxes', 'matantheman', 'ItzDishan', 'Xulfite', 'CinnabonNinja', 'hotrod56478', 'roxo_pl', 'VIPOrder', 'GlowwLikeThat', 'BritishP0litics', 'Nicolas9970', 'YunPlant', 'sirjoshh', 'iMistifye', 'Scorp1x', 'Fribbzdaman', 'xMcKenziee', 'AjinKovac', 'Angels_Develop', 'RonerRehnskiold', 'agnen', 'yusufrad22', 'RocketValkyrie', 'methanshacked', 'GingyWyven', 'KingsmanSS', 'glitch19']
```

* GetUserGroups(UserID) 
```python
robloxpy.GetUserGroups(1368140) #Get a list of groups which the user belongs too
Output > (['Simple Studio', 'BlackRock Studio', 'White Wolf Hounds', '🌶️Hot Pepper Clothes', 'Twisted Murder er Official Group', 'StarCraft®', 'United Alliance Of Roblox', 'NEVER WALK ALONE'], [3297855, 847360, 1201505, 3206677
 1225381, 1132763, 14195, 916576])
```
* # Limited-Functions
These functions relate to getting the value of a user based on their limiteds
* GetUserRAP(UserID)
```python
robloxpy.GetUserRap(1368140) # Get the RAP of the user with the ID 1368140
Output > 298202
```

* GetUserLimitedValue(UserID)
```python
robloxpy.GetUserLimitedValue(1368140) # Get the RAP of the user with the ID 1368140
Output > 389539
```

All the functions to determine the quality of a users items are the same just switching the type each providing a similiar output
* GetUserTerribleDemandLimiteds(UserID)
```python
robloxpy.GetUserTerribleDemandLimiteds(1368140) # Get limiteds considered terrible and undesired by the user with the ID 1368140
Output > 0
```


* ## Group-Functions
These functions allow you to get data in regards to a specific group

IsGroupOwned(GroupID)
```python
robloxpy.IsGroupOwned(916576) # Check if the group of the ID 916576 is owned
Output > True
```
* GetGroupName(GroupID)
```python
robloxpy.GetGroupName(916576) # Get the name of the group of the ID 916576
Output > NEVER WALK ALONE
```

* GetGroupDescription(GroupID)
```python
robloxpy.GetGroupDescription(916576) # Get the description of the group of the ID 916576
Output > [NWA]Never Walk Alone
NWA is a PMC style group that aims for perfection and are looking for all types of members to join to help us with our goal.

We like active members at NWA and have a wide range of bots to help the group function with things such as
 - Automatic Promotion
 - Inactivity Detector

[Automatic Promotions]
{Temp Down Will Be Up Within 1 Week}

[Inactivity Kicked]
{Online - Set to 30 Days}
```

* GetGroupShout(GroupID)
```python
robloxpy.GetGroupShout(916576) # Get the current shout of the group of the ID 916576
Output > How are you?
```

* IsGroupOpen(GroupID)
```python
robloxpy.IsGroupOpen(916576) # Check if the group of the ID 916576 is open to join
Output > True
```

* GetGroupMembers(GroupID)
```python
robloxpy.GetGroupMembers(916576) # Get member count of the group of the ID 916576
Output > 1361
```
* GetGroupAllies(GroupID)
```python
robloxpy.GetGroupAllies(916576) # Get all the allies associated with the group of the ID 916576
Output > ['Akios', 'Dank']
```

* GetGroupEnemies(GroupID)
```python
robloxpy.GetGroupAllies(916576) # Get all the enemies associated with the group of the ID 916576
Output > ['United Alliance Of Roblox']
```

## Asset-Functions
These functions allow you to get data in regards to a specific asset

* CanManage(UserID,AssetID)
```python
robloxpy.CanManage(1368140,240351460)
Output > True
```

# Internal-Functions
These functions require a cookie of the user account they wish to be run on as a variable. These functions allow support for both POST and GET requests allowing actions to be taken on an account.
# Internal-User-Functions
These functions are specific to actions related to the account of the cookies being used.
Since roblox cookies are looooooong I will be using 'ExampleCookie' as a placeholder, below is an example of how you may do this within your program. This cookie is not real and randomly generated following the requirements
```python
ExampleCookie = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_A292F2A0D15508456743D0472FCBF81E081677B96500C348C08C6D3009975DA56D4D1BE762BB225C26A960FEC6746A932C46CFD7364B2F646758731949B6F8C8288F9C628D6AD4DB90C7F1A1BD1EA54AD4169C51AD081561E230C31974366ADEF1726A4490940262EB9D694457C58E48C8385C9D426F0C2A247206DF0E149F675107EB0B60DE5173E5D8556F93CFD6104E786727E6C86A8E8F4CF3B8DEEA0CCE447159BE0D7AB6E16FD193C85526E2BC928F7B90EA5146EC7A243AF98D72EDBCF2154839A8078DAA60F048FFDC67B7367C5E6EE6F7BC5AF902CAB331F66B96310015BB93225E9D4242CD5A4FC2D20321576D268F84A3EBBD752FA80CAF30D73525A9C764FFFE718345EF864235F910EAEB49ED5537AD2432A3A74F9A3AF1B4F5B9C5B2C0'
```

* GetUserName(Cookie)
```python
robloxpy.GetUserName(ExampleCookie) #Get Name of the current cookie in use
Output > Builderman
```

* GetEmail(Cookie)
```python
robloxpy.GetEmail(ExampleCookie) #Get Email of the current cookie in use
Output > Fa********@email.com
```

---
Each of these functions will return a true or false relevant to what is being checked
* IsEmailVerified(Cookie)
* CanTrade(Cookie)
* IsOver13(Cookie)
* IsTwoStepEnabled(Cookie)
* IsAccountPinEnabled(Cookie)
---
* GetRobux(Cookie)
```python
robloxpy.GetUserName(ExampleCookie) #Get Robux of the current cookie in use
Output > 5000
```
* IsPremium(Cookie)
```python
robloxpy.IsPremium(ExampleCookie) #Check if cookie user is premium
Output > True
```

RobloxPy has the ability to follow and unfollow users for the cookie currently being used, these functions will provide a true or false value based on if it was a success; alternatively any errors that occur will be returned to the user also.
* IsFollowing(Cookie, UserID)
```python
robloxpy.IsFollowing(ExampleCookie,1368140) #Check if cookie user is following user with the ID 1368140
Output > True
```

* FollowUser(Cookie, UserID)
```python
robloxpy.FollowUser(ExampleCookie,1368140) #Follow user with ID 1368140
Output > True
```

* UnfollowUser(Cookie, UserID)
```python
robloxpy.UnfollowUser(ExampleCookie,1368140) #Unfollow user with ID 1368140
Output > True
```
RobloxPy has the ability to block and unblock users for the cookie currently being used, these functions will provide a true or false value based on if it was a success; alternatively any errors that occur will be returned to the user also

* BlockUser(Cookie, UserID)
```python
robloxpy.BlockUser(ExampleCookie,1368140) #Block the user with ID 1368140
Output > True
```

* UnblockUser(Cookie, UserID)
```python
robloxpy.UnblockUser(ExampleCookie,1368140) #Unblock the user with ID 1368140
Output > True
```

Robloxpy allows you to send friend requests to users or to unfriend or cancel a friend request. The 'SendFriendRequest' function will provide the output of success or return an error message. The 'Unfriend' function will return either a sent confirmation or error depending on the response from the server.

* SendFriendRequest(Cookie, UserID)
```python
robloxpy.SendFriendRequest(ExampleCookie,1368140) #Send a friend request to the user with ID 1368140
Output > success
```

* Unfriend(Cookie, UserID)
```python
robloxpy.Unfriend(ExampleCookie,1368140) #Unfriend the user with ID 1368140
Output > sent
```

* TotalFriends(Cookie, UserID)
```python
robloxpy.TotalFriends(ExampleCookie) #Total friends of the local user
Output > 5
```

# Internal-Group-Functions
The functions require the use of a cookie that can be used to get the information required.

* ClaimGroup(Cookie,GroupID)
```python
robloxpy.JoinGroup(ExampleCookie,916576) #Claim ownership of group with the ID 916576 if possible
Output > Sent
```

* JoinGroup(Cookie,GroupID)
```python
robloxpy.JoinGroup(ExampleCookie,916576) #Join group with the ID 916576 if possible
Output > Joined
```

* LeaveGroup(Cookie,GroupID)
```python
robloxpy.LeaveGroup(ExampleCookie,916576) #Leave group with the ID 916576 if possible
Output > Left
```

* GetFunds(Cookie,GroupID)
```python
robloxpy.GetFunds(ExampleCookie,916576) #Get funds of 916576 if they can be spent
Output > 583
```

RobloxPy supports the payout of group funds in both a percentage and value capacity. The functions also support a small ammount of error checking confirming if the payment was reported as being sent or not.
* PayGroupFunds(Cookie,GroupID,UserID,RobuxAmmount)
```python
robloxpy.PayGroupFunds(ExampleCookie,916576,1368140,100) #Get 100 robux from group ID 916576 if they can be spent
Output > Sent
```

* PayGroupPercentage(Cookie,GroupID,UserID,RobuxAmmount)
```python
robloxpy.PayGroupPercentage(ExampleCookie,916576,1368140,100) #Get 100 robux from group ID 916576 if they can be spent
Output > Sent
```

* PostGroupWall(Cookie,GroupID,Text)
```python
robloxpy.PostGroupWall(ExampleCookie,916576,'Hello World') #Send a post to the wall of group ID 916576
Output > Sent
```