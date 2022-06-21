import { Settings } from 'components/layout'

function SettingsPage(props) {
    const {setSSH} = props;

    return (
        <>
            <Settings
            setSSH = {setSSH}
            ></Settings>
        </>
    )
}

export default SettingsPage