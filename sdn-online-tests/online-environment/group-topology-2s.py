from mininet.link import TCLink
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.term import makeTerm
from time import sleep
import asyncio


class SingleSwitchTopo(Topo):
    """Single switch connected to n hosts."""

    def build(self):
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')
        s4 = self.addSwitch('s4', protocols='OpenFlow13')

        # add clients
        h1 = self.addHost('h1', mac="00:00:00:00:11:11")
        # h2 = self.addHost('h2', mac="00:00:00:00:11:12")
        h2 = self.addHost('h2', mac="00:00:00:00:11:13")
        h3 = self.addHost('h3', mac="00:00:00:00:11:14")
        h4 = self.addHost('h4', mac="00:00:00:00:11:15")
        h5 = self.addHost('h5', mac="00:00:00:00:11:17")
        h6 = self.addHost('h6', mac="00:00:00:00:11:18")
        h7 = self.addHost('h7', mac="00:00:00:00:11:19")
        h8 = self.addHost('h8', mac="00:00:00:00:11:20")
        h9 = self.addHost('h9', mac="00:00:00:00:11:21")
        h10 = self.addHost('h10', mac="00:00:00:00:11:22")
        h11 = self.addHost('h11', mac="00:00:00:00:11:23")
        h12 = self.addHost('h12', mac="00:00:00:00:11:24")
        h13 = self.addHost('h13', mac="00:00:00:00:11:25")
        h14 = self.addHost('h14', mac="00:00:00:00:11:26")
        h15 = self.addHost('h15', mac="00:00:00:00:11:27")
        # h16 = self.addHost('h16', mac="00:00:00:00:11:28")
        # h17 = self.addHost('h17', mac="00:00:00:00:11:29")
        # h18 = self.addHost('h18', mac="00:00:00:00:11:30")
        # h19 = self.addHost('h19', mac="00:00:00:00:11:31")
        # h20 = self.addHost('h20', mac="00:00:00:00:11:32")
        # # add internet and classifier
        # classifier = self.addHost('classifier')
        inet = self.addHost('i1', mac="00:00:00:00:11:10")

        # --------------------- START DOUBLE SWITCH -----------------------------------------------------------
        # self.addLink(s1, classifier, 1, 1, bw=10, cls=TCLink)
        self.addLink(s1, inet, 1, 1, bw=2, cls=TCLink)

        self.addLink(s1, s2, 2, 1, bw=2, cls=TCLink)
        self.addLink(s2, s3, 2, 1, bw=2, cls=TCLink)
        self.addLink(s2, s4, 3, 1, bw=2, cls=TCLink)

        self.addLink(s3, h1, 2, 1, bw=2, cls=TCLink)
        self.addLink(s3, h2, 3, 1, bw=2, cls=TCLink)
        self.addLink(s3, h8, 4, 1, bw=2, cls=TCLink)
        self.addLink(s3, h9, 5, 1, bw=2, cls=TCLink)
        self.addLink(s3, h10, 6, 1, bw=2, cls=TCLink)
        self.addLink(s3, h11, 7, 1, bw=2, cls=TCLink)
        self.addLink(s3, h12, 8, 1, bw=2, cls=TCLink)


        self.addLink(s4, h3, 2, 1, bw=2, cls=TCLink)
        self.addLink(s4, h4, 3, 1, bw=2, cls=TCLink)
        self.addLink(s4, h5, 4, 1, bw=2, cls=TCLink)
        self.addLink(s4, h6, 5, 1, bw=2, cls=TCLink)
        self.addLink(s4, h7, 6, 1, bw=2, cls=TCLink)
        self.addLink(s4, h13, 7, 1, bw=2, cls=TCLink)
        self.addLink(s4, h14, 8, 1, bw=2, cls=TCLink)
        self.addLink(s4, h15, 9, 1, bw=2, cls=TCLink)
        # self.addLink(s3, h19, 10, 1, bw=10, cls=TCLink)
        # self.addLink(s3, h20, 11, 1, bw=10, cls=TCLink)

        # self.addLink(s1, h11, 12, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h12, 13, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h13, 14, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h14, 15, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h15, 16, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h16, 17, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h17, 18, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h18, 19, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h19, 20, 1, bw=10, cls=TCLink)
        # self.addLink(s1, h20, 21, 1, bw=10, cls=TCLink)


def main():
    setLogLevel('info')
    topo = SingleSwitchTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()
    info("*** Running interactive menu\n")
    user_input = "QUIT"
    # run till user quits
    while True:
        # if user enters CTRL + D then treat it as quit
        try:
            user_input = input("BASE/GEN/CLI/QUIT: ")
        except EOFError as error:
            user_input = "QUIT"

        if user_input.upper() == "GEN":
            switches = net.switches
            hosts = net.hosts
            classifier = switches[1]
            print(classifier)
            makeTerm(classifier, cmd="bash -c 'python classifier.py;'")

            sleep(5)
            for i in range(len(hosts) - 1):
                host = hosts[i]
                client_cmd = "bash -c 'python send_pcaps.py " + host.MAC() + " " + str(i + 1) + ";'"
                print(client_cmd)
                makeTerm(host, cmd=client_cmd)
            makeTerm(switches[0], cmd="bash -c 'python log_stats.py;'")

        elif user_input.upper() == "BASE":
            switches = net.switches
            hosts = net.hosts
            classifier = switches[0]
            print(classifier)
            # makeTerm(classifier, cmd="bash -c 'python base.py;'")
            sleep(5)
            for i in range(len(hosts) - 1):
                host = hosts[i]
                client_cmd = "bash -c 'python send_pcaps.py " + host.MAC() + " " + str(i + 1) + ";'"
                print(client_cmd)
                makeTerm(host, cmd=client_cmd)
            makeTerm(classifier, cmd="bash -c 'python log_stats.py;'")


        elif user_input.upper() == "CLI":
            info("Running CLI...\n")
            CLI(net)

        elif user_input.upper() == "QUIT":
            info("Terminating...\n")
            net.stop()
            break

        else:
            print("Command not found")


if __name__ == '__main__':
    main()
