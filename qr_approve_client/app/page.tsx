"use client"

import { useEffect, useRef, useState } from "react";
import Sidebar from "@/components/ui/SideBar";
import Camera from "@/components/ui/Camera";

export default function Home() {




    return (
        <div className="flex min-s-screen">
            <Sidebar />
            <main className="mx-4">
                <div className="flex flex-row">
                    <Camera />
                </div>
            </main>


        </div>
    );
}
