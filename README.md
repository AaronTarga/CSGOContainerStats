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
2. Retrieve steam cookie
3. Enter cookie in example_profile.yaml file(see [example file](example_profile.yaml))
4. Rename example_profile.yaml to profile.yaml
4. Execute calculate python script and wait for it to finish (python calculate.py)
5. Stats are now written in stats.txt file from the directory where you executed the script

### Arguments

There are different arguments that can be viewed calling help.
> python calculate.py help

With the modes flag you can set that the script backups the progress of parsing:
> python calculate.py -m backup

If your script crashes you can continue from where it was using continue mode:
> python calculate.py -m continue

You can add --json or -j to the script to get a json output.
> python calculate.py --json

## Example Result
Here is an example for an output file of the script for the normal format:
```
Case:
    Danger Zone Case:
        26 Mar, 2020 - StatTrak™ SG 553 | Danger Close (Field-Tested) - Mil-Spec Grade
        Summary:
            Mil-Spec Grade: 1/1(100.00%)

Case Summary:
    Mil-Spec Grade: 1/1(100.00%)

Others:
    2020 RMR Legends:
        24 Mar, 2021 - Sticker | Vitality | 2020 RMR - High Grade
        Summary:
            High Grade: 1/1(100.00%)

    2020 RMR Contenders:
        24 Mar, 2021 - Sticker | ESPADA | 2020 RMR - High Grade
        Summary:
            High Grade: 1/1(100.00%)

    Poorly Drawn Capsule:
        24 Mar, 2021 - Sticker | Poorly Drawn FBI (Holo) - Remarkable
        Summary:
            Remarkable: 1/1(100.00%)

    CS20 Sticker Capsule:
        4 Jun, 2020 - Sticker | Nuke Beast - High Grade
        4 Jun, 2020 - Sticker | Nuke Beast - High Grade
        Summary:
            High Grade: 2/2(100.00%)

    Berlin 2019 Minor Challengers (Holo/Foil):
        4 Jun, 2020 - Sticker | Grayhound Gaming (Holo) | Berlin 2019 - Remarkable
        4 Jun, 2020 - Sticker | CR4ZY (Foil) | Berlin 2019 - Exotic
        Summary:
            Remarkable: 1/2(50.00%)
            Exotic: 1/2(50.00%)

    Skill Groups Capsule:
        4 Jun, 2020 - Sticker | Distinguished Master Guardian - High Grade
        Summary:
            High Grade: 1/1(100.00%)

    Berlin 2019 Legends Autograph Capsule:
        4 Jun, 2020 - Sticker | Golden | Berlin 2019 - High Grade
        4 Jun, 2020 - Sticker | rain (Foil) | Berlin 2019 - Remarkable
        Summary:
            High Grade: 1/2(50.00%)
            Remarkable: 1/2(50.00%)

    Half-Life: Alyx Sticker Capsule:
        26 Mar, 2020 - Sticker | Lambda (Holo) - Remarkable
        26 Mar, 2020 - Sticker | Lambda - High Grade
        Summary:
            Remarkable: 1/2(50.00%)
            High Grade: 1/2(50.00%)

Others Summary:
    High Grade: 7/12(58.33%)
    Remarkable: 4/12(33.33%)
    Exotic: 1/12(8.33%)
```

Here is an example for an output file of the script for the json format:

```
{
    "Case": {
        "items": {
            "Danger Zone Case": {
                "items": [
                    "26 Mar, 2020 - StatTrak\u2122 SG 553 | Danger Close (Field-Tested) - Mil-Spec Grade"
                ],
                "summary": {
                    "Mil-Spec Grade": {
                        "absolute": 1,
                        "relative": 100.0
                    }
                },
                "count": 1
            }
        },
        "summary": {
            "Mil-Spec Grade": {
                "absolute": 1,
                "relative": 100.0
            }
        },
        "count": 1
    },
    "Others": {
        "items": {
            "2020 RMR Legends": {
                "items": [
                    "24 Mar, 2021 - Sticker | Vitality | 2020 RMR - High Grade"
                ],
                "summary": {
                    "High Grade": {
                        "absolute": 1,
                        "relative": 100.0
                    }
                },
                "count": 1
            },
            "2020 RMR Contenders": {
                "items": [
                    "24 Mar, 2021 - Sticker | ESPADA | 2020 RMR - High Grade"
                ],
                "summary": {
                    "High Grade": {
                        "absolute": 1,
                        "relative": 100.0
                    }
                },
                "count": 1
            },
            "Poorly Drawn Capsule": {
                "items": [
                    "24 Mar, 2021 - Sticker | Poorly Drawn FBI (Holo) - Remarkable"
                ],
                "summary": {
                    "Remarkable": {
                        "absolute": 1,
                        "relative": 100.0
                    }
                },
                "count": 1
            },
            "CS20 Sticker Capsule": {
                "items": [
                    "4 Jun, 2020 - Sticker | Nuke Beast - High Grade",
                    "4 Jun, 2020 - Sticker | Nuke Beast - High Grade"
                ],
                "summary": {
                    "High Grade": {
                        "absolute": 2,
                        "relative": 100.0
                    }
                },
                "count": 2
            },
            "Berlin 2019 Minor Challengers (Holo/Foil)": {
                "items": [
                    "4 Jun, 2020 - Sticker | Grayhound Gaming (Holo) | Berlin 2019 - Remarkable",
                    "4 Jun, 2020 - Sticker | CR4ZY (Foil) | Berlin 2019 - Exotic"
                ],
                "summary": {
                    "Remarkable": {
                        "absolute": 1,
                        "relative": 50.0
                    },
                    "Exotic": {
                        "absolute": 1,
                        "relative": 50.0
                    }
                },
                "count": 2
            },
            "Skill Groups Capsule": {
                "items": [
                    "4 Jun, 2020 - Sticker | Distinguished Master Guardian - High Grade"
                ],
                "summary": {
                    "High Grade": {
                        "absolute": 1,
                        "relative": 100.0
                    }
                },
                "count": 1
            },
            "Berlin 2019 Legends Autograph Capsule": {
                "items": [
                    "4 Jun, 2020 - Sticker | Golden | Berlin 2019 - High Grade",
                    "4 Jun, 2020 - Sticker | rain (Foil) | Berlin 2019 - Remarkable"
                ],
                "summary": {
                    "High Grade": {
                        "absolute": 1,
                        "relative": 50.0
                    },
                    "Remarkable": {
                        "absolute": 1,
                        "relative": 50.0
                    }
                },
                "count": 2
            },
            "Half-Life: Alyx Sticker Capsule": {
                "items": [
                    "26 Mar, 2020 - Sticker | Lambda (Holo) - Remarkable",
                    "26 Mar, 2020 - Sticker | Lambda - High Grade"
                ],
                "summary": {
                    "Remarkable": {
                        "absolute": 1,
                        "relative": 50.0
                    },
                    "High Grade": {
                        "absolute": 1,
                        "relative": 50.0
                    }
                },
                "count": 2
            }
        },
        "summary": {
            "High Grade": {
                "absolute": 7,
                "relative": 58.333333333333336
            },
            "Remarkable": {
                "absolute": 4,
                "relative": 33.33333333333333
            },
            "Exotic": {
                "absolute": 1,
                "relative": 8.333333333333332
            }
        },
        "count": 12
    }
}
```

## FAQ

How to retrieve Cookies?

Using extension(easy):

1. Download [Cookie Editor]((https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)) for Firefox or [Cookie Editor](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=de) for Chrome
2. Go to steam site and log in
3. Click on cookie editor extension icon or press F12 and click on EditThisCookie/Cookie Editor Tab
4. Copy needed cookie value

Using browser:

1. Go to steam site and log in
2. Press F12
3. Go to Network Tab
4. Press F5 to refresh site
5. Select the top entry at the network tab
6. Scroll down on the right side till you see Cookie
7. Copy needed cookie value

Script crashes with following message: "Couldn't fetch pages possibly to steam network error.".

**Tl;dr: Try to start the script again!**

What probably happened:
- Steam blocked your IP. This is unlikely to happen because the script only sends a few requests each minute.
- Your Cookie expired. If you restart the script it should detect the expired cookies and display a message that informs you to fetch new cookies.
- There was some sort of network error like the message says. In this case you should try to start the script again.