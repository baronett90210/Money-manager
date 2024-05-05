<img src = "https://github.com/baronett90210/Money-manager/assets/136889949/e8626b3f-5cad-45bd-baf3-0295ba086d91" width="40" height="40">    $\bf{This\ is\ a\ budget\ tool}$ developed by me for personal purposes and of course for fun :). I would be very happy if somebody tries it out. Suggestions/bug fixes are welcome!
To run an example: Simple_run.py

<img src = "https://github.com/baronett90210/Money-manager/assets/136889949/fd77a708-cab5-45d8-b6bc-0d8b0ac976bc" width="40" height="40">  Upon the first run, spending.csv file is created in the folder. It contains fixed monthly expenses, like rental, utilities etc and income. To change, go to app/tool.py, line 37

![image](https://github.com/baronett90210/Money-manager/assets/136889949/b1e5f816-7162-44fc-b33e-a0a2da41f179)

$\bf{The\ general\ layout}$ is presented below

<img src = "https://github.com/baronett90210/Money-manager/assets/136889949/3ec1fcca-cbd8-4cf7-9b9c-f33c762ce3f1" width="800" height="600">

The left bar plot visualizes expenses by categories in a given month selected in the box above. The right figure shows the monthly spending or income corresponding to selected category.

<img src = "https://github.com/baronett90210/Money-manager/assets/136889949/c56ef2d4-75f9-411b-925f-41a509125b2d" width="40" height="40">  You may $\bf{add\ spending\ or\ income}$ in corresponding boxes and press Capture buttons. The plots will be updated automatically.

![image](https://github.com/baronett90210/Money-manager/assets/136889949/7fc55034-b4e5-4287-8d9d-1a73347e39a2) ![image](https://github.com/baronett90210/Money-manager/assets/136889949/a6f1a753-047a-4227-8fe3-212641418453)

<img src = "https://github.com/baronett90210/Money-manager/assets/136889949/5735333c-13d9-4fac-9c77-9023e0d6c322" width="40" height="40">  $\bf{The\ goal\ box}$ displays the balance counted from the starting date and how far we are from our financial goal. To change the date and the goal use SET! buttons.

There is an $\bf{option\ to\ modify\ the\ data\ manually}$ in case of an incorrect input. Press Display data button and you will see the whole table which you may edit. Upon closing the table, the app asks you if you want to save the modified data. 

![image](https://github.com/baronett90210/Money-manager/assets/136889949/0a6ae393-330d-4782-bfd9-01d5c4024190)


Note that I have included an $\bf{option to use spending.csv file on Google Drive}$ which gives an oppotrunity to add the expenses by multiple users. However, for that you need to set up the Drive to get client_secrets.json. If there is an interest I will post the instructions.
