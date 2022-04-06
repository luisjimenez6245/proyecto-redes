import { Link } from 'react-router-dom'

function Menu(props) {
    const { path } = props
    return (
        <>
            <section className="hero is-fullheight p-0 m-0">
                <div className="hero-head">

                    <aside className="menu ml-2">
                    
                        <p className="menu-label">
                            General
                        </p>
                        <ul className="menu-list">
                            <li>
                                <Link to='/home/contents' className={`is-size-6 ${(path === 'contents') ? 'is-active' : ''}`}>
                                    Páginas
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