FROM debian
RUN apt update
RUN apt install git -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt clean
RUN git clone https://github.com/personal-army-of-4o/nyanMigen.git
RUN git clone https://github.com/nmigen/nmigen.git
RUN cd nyanMigen && git checkout add_setup_deps && pip3 install .
RUN cd nmigen && pip3 install .
ENV PYTHONPATH=/nyanMigen/
