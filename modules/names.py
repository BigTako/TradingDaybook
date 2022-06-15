
assetsNames = ["EUR USD", "GBP USD", "AUD USD", "EUR AUD", "USD CHF", "USD CAD",
               "EUR JPY", "EUR GBP", "EUR CAD", "EUR NZD", "GBP AUD", "GBP CAD",
               "GBP JPY", "GBP NZD", "AUD CHF", "CAD JPY", "CHF JPY", "NZD CAD",
               "NZD JPY", "NZD USD", "USD JPY", "AUD JPY", "NZD CHF", "CAD CHF",
               "AUD NZD", "USD NOK", "AUD CAD", "CHF JPY", "Silver", "Gold", "BRENT",
               "CC", "AC", "Bitcoin", "Ethereum", "Dow Jones", "Nasdaq", "Copper",
               "Platinum"]

figures = { "Straight triangle": 0, "Down triangle": 0, "Upware triangle": 0, "Flat": 0, "Down trend": 0,
            "Upware trend": 0,"Bullish flag": 0, "Bearish flag": 0, "Failled sweep(top)": 0, "Failed sweep(bottom)": 0,
            "Ikigai Box(top)": 0, "Ikigai Box(bottom)": 0, "2le Top": 0, "2le Bottom": 0, "3le Top": 0, "3le Buttom": 0}

patterns = {"hammer": 0, "hanged man": 0, "bull abc.": 0,"bear abc.": 0, "clear clouds": 0, "dark clouds": 0,
            "railways(top)": 0, "railways(bottom)": 0, "reversed hammer": 0,"bull line pen.": 0, "bear line pen.": 0,
            "top harami": 0, "bottom harami": 0, "evening star": 0, "morning star": 0}

direction = {"to break up": 0, "to break down": 0, "turn down": 0,
             "turn up": 0, "correction down": 0, "correction up": 0}

indicator = {"upper cross": 0, "down cross": 0, "inters. from top": 0, "inters. from buttom": 0,
            "top compression": 0, "bottom compression": 0}

columns = ["id","date", "time", "news", "moneym", "riskm", "asset", "exptime", "result", "situation", "url",
                  "details"]

table_cols = ["date", "time", "news", "moneym", "riskm", "asset", "exptime", "result", "situation", "url",
             "details"]

periods_dict = {"5-8": 0, "8-11": 0, "11-14": 0, "14-17": 0, "17-20": 0}