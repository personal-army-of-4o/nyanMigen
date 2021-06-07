FROM debian
RUN apt update && apt install git python3 python3-pip -y && apt-get autoclean && apt-get clean && apt-get -y autoremove && \
git clone https://github.com/personal-army-of-4o/nyanMigen.git && \
git clone https://github.com/personal-army-of-4o/nmigen.git && \
git clone https://github.com/personal-army-of-4o/cocotb_helper.git && \
git clone https://github.com/personal-army-of-4o/python_mm.git && \
cd nyanMigen && pip3 install . && cd .. && \
cd nmigen && git checkout b7e2da704d9651544808f91fb380ed3f6d05fb14 && pip3 install . && cd .. && \
cd cocotb_helper && git checkout nmigen_port && cd .. && \
pip3 install pprintast astunparse
ENV PYTHONPATH=/cocotb_helper/:/nyanMigen/:/python_mm/
