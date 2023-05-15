import rospy
import smach

class Estado1(smach.State):
    def __init__(self) -> None:
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.couner = 0

    def execute(self, userdata):
        if self.couner < 3:
            self.couner += 1
            return 'outcome1'
        else:
            return 'outcome2'


class Estado2(smach.State):
    def __init__(self) -> None:
        smach.State.__init__(self, outcomes=['outcome2'])
    def execute(self, userdata):
        return 'outcome2'

def main():
    rospy.init_node('controlessss')
    sm = smach.StateMachine(outcomes=['outcome4', 'outcome5'])
    with sm:
        smach.StateMachine.add('Estado 1', Estado1(),
                               transitions={
                                   'outcome1': 'Estado 2',
                                   'outcome2': 'outcome4'
                                   })
        smach.StateMachine.add('Estado 2', Estado2(),
                               transitions={
                                   'outcome2': 'Estado 1'
                                   })
    outcome = sm.execute()
    print(outcome)
if __name__=='__main__':
    main()
