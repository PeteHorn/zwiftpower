Requires a venv to be created and the python requirements to be installed. Then create a .sh file somewhere which is something like

```
cd /home/pete/Documents/zwift_power
source venv/bin/activate
python3 src/zp.py --email "xxx@gmail.com" --password xxxxxxxx --url "https://zwiftpower.com/profile.php?z=xxxxxxx" --folder "/home/pete/Documents/testdata" --filename Pete_Horn --destination "/home/pete/Documents/testdata/graphs/" --log "/home/pete/Documents/testdata/log/zp.log"
```

Still working on improving the code base
