"use client"

//import library
import { useState } from "react"
import { FaHome, FaCamera, FaVideo, FaCog } from 'react-icons/fa';


export default function SideBar() {
    const [isOpen, setIsOpen] = useState(false)

    return (
        <div className={`fixed  inset-y-0 left-0 w-64 bg-gray-600 text-white transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-200 ease-in-out md:translate-x-0 md:relative h-screen`}>
            <div className="p-4">
                <h1 className="text-2xl font-bold">PAYMENT DETECTION</h1>
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="md:hidden absolute top-2 right-2 p-2 bg-gray-700 rounded"
                >
                    {isOpen ? 'Close' : 'Menu'}
                </button>
            </div>
            <nav className="mt-4">
                <ul>
                    <li className="p-2 hover:bg-gray-700">
                        <a href="#" className="flex items-center">
                            <FaHome className="mr-2" />
                            Detection
                        </a>
                    </li>
                    <li className="p-2 hover:bg-gray-700">

                        <a href="#" className="flex items-center">
                            <FaCog className="mr-2" />
                            Settings
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    )
} 