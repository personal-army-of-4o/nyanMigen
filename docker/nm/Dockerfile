FROM debian
RUN apt update
RUN apt install git -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt clean
RUN git clone https://github.com/personal-army-of-4o/nyanMigen.git
RUN git clone https://github.com/personal-army-of-4o/nmigen.git
RUN git clone https://github.com/personal-army-of-4o/cocotb_helper.git
RUN cd nyanMigen && git checkout a32309a953a6d504231ce399ea09cfdef5a31803 && pip3 install .
RUN cd nmigen && git checkout b7e2da704d9651544808f91fb380ed3f6d05fb14 && pip3 install .
RUN cd cocotb_helper && git checkout nmigen_port
RUN pip3 install pprintast astunparse
ENV PYTHONPATH=/cocotb_helper/:/nyanMigen/
