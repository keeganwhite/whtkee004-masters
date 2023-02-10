# QoS with ONOS
Steps to run QoS experiments.

Vist the ONOS Docs [here](http://127.0.0.1:8181/onos/v1/docs/) and the GUI [here]()
## Set up ONOS
### Install Bazel
Download the build script from the releases page on Bazel's GitHub (v3.7.2 for 2.7.0 LTS) and run
```
chmod +x bazel-version-installer-linux-x86_64.sh
./bazel-version-installer-linux-x86_64.sh --user
```

### Setup IntelliJ
For an easier install of ONOS clone the repo, checkout version 2.7.0, change the branch so you can save your commits
then follow the IntelliJ import example [here](https://wiki.onosproject.org/pages/viewpage.action?pageId=28836246). I
had to update my Bazel settings to have the Bazel Binary Location set to ```/home/kwhite/bin/bazel``` where ```kwhite```
is your username.

Once I had finished the linked steps I ran
```
bazel build onos
```

Finally, I ran the unit tests from the root folder
```
bazel query 'tests(//...)' | xargs bazel test
```

I had 3 tests fail that seemed to be linked to K8

## Creating new files/apps
If you check out a different branch with different targets, you might want to update your existing .bazelproject file
to reflect the changes:
```
cd tools/dev/bin/
./onos-gen-bazel-project > ../../../.ijwb/.bazelproject
```
This will replace the project file previously created during the import process. To load the new .bazelproject file
and re-sync your project, in the top menu select:
```
Bazel > Sync > Sync project with BUILD files
```
It should take only a few seconds to re-sync the project after the first import.

## Mininet and Python
- Make sure your switches are set to have their protocol to OpenFlow 1.3
```
s1 = self.addSwitch('s1', protocols='OpenFlow13')
```
### Starting Mininet, starting ONOS, Setting up and Testing the Environment
- Start ONOS (from root)
```
bazel run onos-local clean debug
```
- Attach the CLI when the server has started (from root)
```
tools/test/bin/onos localhost
```
- Before running your Mininet environment make sure to enable OpenFlow and reactive forwarding in ONOS via the CLI
```
app activate org.onosproject.openflow
app activate org.onosproject.fwd 
```
- Navigate to the location of the Mininet python file and run
```
sudo python topo.py
```
_Where topo.py is the python file containing your mininet environment_
- Test the environment by running the following on the Mininet CLI
```
pingall
```
- Set up the flow entry to forward traffic to the classifier with a POST request to the ONOS flow endpoint or run classifier on switch:
```
{
  "flows": [
{
  "priority": 40000,
  "timeout": 0,
  "isPermanent": true,
  "deviceId": "of:0000000000000001",
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": "1"
      }
    ]
  },
  "selector": {
    "criteria": [
      {
        "type": "IN_PORT",
        "port": "3"
      }

    ]
  }
}
]
}
```
- Test this works by starting Wireshark
```
sudo wireshark &
```
select the switch ones first port and ping the 'internet' from another host
```
h1 ping inet
```
and you should see the packets showing up on the classifiers interface on Wireshark.