# Personal Cloud
personal-cloud (as a reference to [Personal Computer](https://en.wikipedia.org/wiki/Personal_computer) / PC) is a collection of [How-To](howto.md) that we developed at [April Software](https://www.aprilsoftware.com/) to run our software stack. We think it could benefit to others to install and operate a [Personal Cloud](pc-manifesto.md).

We decided to run our own IT infrastructure based on the principle of being as less as possible dependent on commercial software or commercially supported open source software. 
There are pro and cons using commercial software or open source software. We believe in open source and to the power of the community. We think that it is the most sustainable approach to support long term businesses.

The open source ecosystem is very rich and provides everything you would need to build your own infrastructure. There are almost endless possibilities and picking up the different components that you would need to build your own infrastructure could be a challenging task.

We selected [Debian](https://www.debian.org/) as operating system. There are very good alternatives to Debian; which are eventually backed by commercial companies. However Debian fits with the principle of being as less as possible dependent on commercial software and commercially supported open source software. Even do they remain open source software, some other distributions are governed mainly by the companies that support them. On the other end, Debian is governed by the Debian community. Again there are pro and cons and we can debate it years. Our intention here is about sharing the knowledge we collected over the years operating the software stack we built.

We selected [GlusterFS](https://www.gluster.org/) for the storage, for its simplicity and its reliability. 

The first brick of the infrastructure is what we called a [Personal Cluster](personal-cluster.md) (Here also as a reference to PC, the three PC acronyms being a different layer of abstraction). A Personal Cluster takes care of VMs and their Storage in a high availability way. From there we deploy Kubernetes Clusters and cloud services.

Building a cluster requires you to have several computers available. The minimum is 2 and the more is the better. However the number of computers follows the rules given by GlusterFS. Depending on the number of replica you would like to keep, it should be a multiple of it. For instance, you could have a cluster or 2, 4, 6, x nodes storing 2 replicas or most probably 3, 6, 9, x storing 3 replicas (to avoid [Split-Brains](https://docs.gluster.org/en/main/Administrator-Guide/Split-brain-and-ways-to-deal-with-it/)).

Start by installing your first [Personal Cluster](personal-cluster.md) to operate your first [Personal Cloud](pc-manifesto.md).

We learned a lot during that journey and we hope that you will enjoy it.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.md)