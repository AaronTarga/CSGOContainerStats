# CSGOContainerStats

This Python script parses the steam inventory history for unboxed csgo items from containers like cases, souvenir, packages,sticker capsules and so on.
If the script doesn't crash or get's stopped, it writes all unboxed items grouped by container where they got unboxed from into a file called stats.txt.

## Requirements

- A steam account with inventory history of csgo items  
- At least Python version 3.6 installed. The newest Python version at the official Python's [site](https://www.python.org/downloads/).
- Python needs to have pip module installed, see [website](https://pip.pypa.io/en/stable/installing/) of pip module for installation.

After you have Python and pip installed you can install all needed dependencies with this command:
```
pip install -r requirements.txt
```

## Usage

1. Check that all requirements are fulfilled
2. Retrieve steam cookies
3. Enter cookies in profile.yaml file(see Example Config)
4. Execute python script and wait for it to finish 
5. Stats are now written in stats.txt file from the directory where you executed the script

## Example Config
Here is an example for the profile.yaml needed:
```
sessionid: "retrieved-sessionid"
steamLoginSecure: "retrieved-loggin-secure"
```

## Example Result
Here is an example for an output file of the script:
```
Autograph Capsule | Fnatic | Cologne 2015:
   Sticker | KRIMZ | Cologne 2015 - High Grade

   Summary:
       High Grade: 1/1(100.0%)

Operation Breakout Weapon Case:
   Negev | Desert-Strike (Field-Tested) - Mil-Spec Grade
   UMP-45 | Labyrinth (Minimal Wear) - Mil-Spec Grade
   StatTrak™ SSG 08 | Abyss (Minimal Wear) - Mil-Spec Grade
   Negev | Desert-Strike (Factory New) - Mil-Spec Grade

   Summary:
       Mil-Spec Grade: 4/4(100.0%)

Chroma 2 Case:
   M4A1-S | Hyper Beast (Well-Worn) - Covert
   P250 | Valence (Field-Tested) - Mil-Spec Grade
   AWP | Worm God (Minimal Wear) - Restricted
   Five-SeveN | Monkey Business (Well-Worn) - Classified

   Summary:
       Covert: 1/4(25.0%)
       Mil-Spec Grade: 1/4(25.0%)
       Restricted: 1/4(25.0%)
       Classified: 1/4(25.0%)

Chroma Case:
   StatTrak™ M249 | System Lock (Field-Tested) - Mil-Spec Grade
   Glock-18 | Catacombs (Field-Tested) - Mil-Spec Grade
   StatTrak™ Glock-18 | Catacombs (Field-Tested) - Mil-Spec Grade
   M249 | System Lock (Minimal Wear) - Mil-Spec Grade

   Summary:
       Mil-Spec Grade: 4/4(100.0%)

Operation Phoenix Weapon Case:
   MAG-7 | Heaven Guard (Minimal Wear) - Mil-Spec Grade

   Summary:
       Mil-Spec Grade: 1/1(100.0%)

Final Summary:
   High Grade: 1/14(7.142857142857142%)
   Mil-Spec Grade: 10/14(71.42857142857143%)
   Covert: 1/14(7.142857142857142%)
   Restricted: 1/14(7.142857142857142%)
   Classified: 1/14(7.142857142857142%)
```

## FAQ

How to retrieve Cookies?

Using extension(easy):

1. Download [Cookie Editor]((https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)) for Firefox or [Cookie Editor](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=de) for Chrome
2. Go to steam site and log in
3. Click on cookie editor extension icon or press F12 and click on EditThisCookie/Cookie Editor Tab
4. Copy needed cookie values

Using browser:

1. Go to steam site and log in
2. Press F12
3. Go to Network Tab
4. Press F5 to refresh site
5. Select the top entry at the network tab
6. Scroll down on the right side till you see Cookie
7. Copy needed values