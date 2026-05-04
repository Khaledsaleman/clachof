import React, { useEffect, useState } from 'react';
import WebApp from '@twa-dev/sdk';
import { TonConnectButton, useTonAddress } from '@tonconnect/ui-react';
import axios from 'axios';
import { Home, Swell as Sword, Shield, Users, Wallet } from 'lucide-react';

const API_BASE = 'http://localhost:8000'; // Change to production URL

function App() {
  const [user, setUser] = useState<any>(null);
  const [activeTab, setActiveTab] = useState('base');
  const address = useTonAddress();

  useEffect(() => {
    WebApp.ready();
    const initData = WebApp.initData;

    axios.post(`${API_BASE}/users/me`, {}, {
      headers: { 'Authorization': `Bearer ${initData}` }
    }).then(res => {
      setUser(res.data);
    }).catch(err => {
      console.error("Auth failed", err);
      // Fallback for dev
      setUser({ username: 'Player', gold: 1000, energy: 100, rank: 0, buildings: [], units: [] });
    });
  }, []);

  useEffect(() => {
    if (address && user) {
      axios.post(`${API_BASE}/wallet/connect?address=${address}`, {}, {
        headers: { 'Authorization': `Bearer ${WebApp.initData}` }
      });
    }
  }, [address]);

  return (
    <div className="min-h-screen bg-slate-900 text-white font-sans pb-20">
      {/* Header */}
      <div className="bg-slate-800 p-4 flex justify-between items-center sticky top-0 z-10 border-b border-slate-700">
        <div>
          <h1 className="text-xl font-bold text-yellow-500">TCOC</h1>
          <p className="text-xs text-slate-400">@{user?.username || 'Guest'}</p>
        </div>
        <div className="flex gap-4 items-center">
          <div className="text-right">
            <p className="text-sm font-bold text-yellow-400">💰 {user?.gold?.toLocaleString()}</p>
            <p className="text-xs text-blue-400">⚡ {user?.energy}/100</p>
          </div>
          <TonConnectButton />
        </div>
      </div>

      {/* Main Content */}
      <div className="p-4">
        {activeTab === 'base' && (
          <div className="space-y-6">
            <div className="bg-slate-800 p-4 rounded-xl border border-slate-700">
              <h2 className="text-lg font-bold mb-4">My Village</h2>
              <div className="grid grid-cols-3 gap-4">
                {user?.buildings.map((b: any) => (
                  <div key={b.id} className="bg-slate-700 p-3 rounded-lg text-center">
                    <p className="text-xs uppercase font-bold text-slate-400">{b.type}</p>
                    <p className="text-lg">Lv. {b.level}</p>
                  </div>
                ))}
                <button className="bg-blue-600 p-3 rounded-lg text-center flex flex-col items-center justify-center border-2 border-dashed border-blue-400 opacity-80">
                  <span className="text-2xl">+</span>
                  <span className="text-xs">Build</span>
                </button>
              </div>
            </div>

            <div className="bg-slate-800 p-4 rounded-xl border border-slate-700">
              <h2 className="text-lg font-bold mb-4">My Army</h2>
              <div className="flex gap-4 overflow-x-auto pb-2">
                {user?.units.map((u: any) => (
                  <div key={u.type} className="bg-slate-700 p-3 rounded-lg min-w-[100px] text-center">
                    <p className="text-xs font-bold text-slate-400">{u.type}</p>
                    <p className="text-xl">x{u.count}</p>
                  </div>
                ))}
                <button className="bg-green-600 px-4 rounded-lg">Train</button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'battle' && (
          <div className="space-y-4">
            <h2 className="text-xl font-bold">Battle Arena</h2>
            <p className="text-slate-400">Find an opponent to loot resources!</p>
            <button className="w-full bg-red-600 py-4 rounded-xl font-bold text-lg shadow-lg shadow-red-900/20 active:scale-95 transition-transform">
              FIND OPPONENT (10 ⚡)
            </button>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-slate-800 border-t border-slate-700 flex justify-around p-2">
        <button onClick={() => setActiveTab('base')} className={`flex flex-col items-center p-2 ${activeTab === 'base' ? 'text-yellow-500' : 'text-slate-400'}`}>
          <Home size={24} />
          <span className="text-[10px] mt-1">Base</span>
        </button>
        <button onClick={() => setActiveTab('battle')} className={`flex flex-col items-center p-2 ${activeTab === 'battle' ? 'text-yellow-500' : 'text-slate-400'}`}>
          <Sword size={24} />
          <span className="text-[10px] mt-1">Attack</span>
        </button>
        <button onClick={() => setActiveTab('clan')} className={`flex flex-col items-center p-2 ${activeTab === 'clan' ? 'text-yellow-500' : 'text-slate-400'}`}>
          <Users size={24} />
          <span className="text-[10px] mt-1">Clans</span>
        </button>
        <button onClick={() => setActiveTab('wallet')} className={`flex flex-col items-center p-2 ${activeTab === 'wallet' ? 'text-yellow-500' : 'text-slate-400'}`}>
          <Wallet size={24} />
          <span className="text-[10px] mt-1">Assets</span>
        </button>
      </div>
    </div>
  );
}

export default App;
