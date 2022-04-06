import { Link } from 'react-router-dom'

function Menu(props) {
    const { path } = props
    return (
        <>
            <section className="hero is-fullheight pt-3 m-0">
                <div className="hero-head">
                    <aside className="menu ml-2">
                        <p className="menu-label">
                            General
                        </p>
                        <ul className="menu-list">
                            <li>
                                <Link to='/home' className={`is-size-6 ${(path === '') ? 'is-active' : ''}`}>
                                    Principal
                                </Link>
                            </li>
                            <li>
                                <Link to='/home/users' className={`is-size-6 ${(path === 'users') ? 'is-active' : ''}`}>
                                    Usuarios
                                </Link>
                            </li>
                            <li>
                                <Link to='/home/devices' className={`is-size-6 ${(path === 'devices') ? 'is-active' : ''}`}>
                                    Dispositvos
                                </Link>
                            </li>
                        </ul>
                    </aside>
                </div>
            </section>
        </>
    )
}
export default Menu