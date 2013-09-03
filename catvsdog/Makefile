### Macros ###
MAIN		= catvsdog.py
TESTDIR		= testfiles
TESTOUTS	= $(wildcard $(TESTDIR)/*.out)

DFLAGS		= -q
#DFLAGS		= -y

### Targets ###
# target: test - Test all files found in the testfile directory.
test :  $(TESTOUTS:.out=.test)

%.test : %.in
	./$(MAIN) < $< 2>&1 | diff $(DFLAGS) $*.out -
