import React, {useEffect, useState} from 'react';
import NextSelectionButton from '../../ui-components/inline-selection/NextSelectionButton';
import LocalManualRunOptions from './RunManually/LocalManualRunOptions';
import {faLaptopCode} from '@fortawesome/free-solid-svg-icons/faLaptopCode';
import InlineSelection from '../../ui-components/inline-selection/InlineSelection';
import {cloneDeep} from 'lodash';
import {faExpandArrowsAlt} from '@fortawesome/free-solid-svg-icons';
import RunOnIslandButton from './RunOnIslandButton';
import AWSRunButton from './RunOnAWS/AWSRunButton';
import {getAllMachines, getIslandIPsFromMachines} from '../../utils/ServerUtils';

function RunOptions(props) {

  const [currentContent, setCurrentContent] = useState(loadingContents());
  const [ips, setIPs] = useState([]);
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    if (initialized === false) {
      getAllMachines().then(machines => {
        setIPs(getIslandIPsFromMachines(machines));
        setInitialized(true);
      });
    }
  });

  useEffect(() => {
    setCurrentContent(getDefaultContents());
  }, [initialized])

  function setComponent(component, props) {
    if (component === undefined) {
      setCurrentContent(getDefaultContents())
    } else {
      setCurrentContent(component({...props}))
    }
  }

  function loadingContents() {
    return (<div>Loading</div>)
  }

  function getDefaultContents() {
    const newProps = cloneDeep({...props});
    return InlineSelection(defaultContents, newProps);
  }

  function isNotRansomwareMode(islandMode){
    return islandMode !== 'ransomware';
  }

  function defaultContents(props) {
    return (
      <>
        <RunOnIslandButton title={'From Island'}
                           description={'Start on Monkey Island server.'}
                           icon={faExpandArrowsAlt}/>
        <NextSelectionButton title={'Manual'}
                             description={'Run on a machine via command.'}
                             icon={faLaptopCode}
                             onButtonClick={() => {
                               setComponent(LocalManualRunOptions,
                                 {ips: ips, setComponent: setComponent})
                             }}/>
        {isNotRansomwareMode(props.islandMode) && <AWSRunButton setComponent={setComponent}/> }
      </>
    );
  }

  return currentContent;
}

export default RunOptions;
