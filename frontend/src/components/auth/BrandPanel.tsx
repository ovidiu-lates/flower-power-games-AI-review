const stats = [
    { value: '12,400+', label: 'Reviews analyzed' },
    { value: '1,200+', label: 'Games covered' },
    { value: '94%', label: 'AI confidence' },
];

export default function BrandPanel() {
    return (
        <div className= "hidden lg:flex flex-col justify-between w-[480px] bg-[#1C1917] p-12" >
        <div className="flex items-center gap-3" >
            <div className="w-10 h-10 rounded-xl bg-[#C85A1E] flex items-center justify-center" >
          *
                </div>

                < div >
                <p className="text-white font-semibold text-lg" >
                    Flower Power Games
                        </p>
                        < p className = "text-white/50 text-xs" >
                            AI Review Platform
                                </p>
                                </div>
                                </div>

                                < div >
                                <h2 className="text-4xl font-bold text-white mb-4" >
                                    Discover games through real player insights.
        </h2>

                                        < p className = "text-white/60" >
                                            Thousands of reviews analyzed by AI to help you find your next
          favorite board game.
        </p>

        < div className = "grid grid-cols-3 gap-6 mt-10" >
        {
            stats.map((stat) => (
                <div key= { stat.label } >
                <p className="text-2xl font-bold text-white" >
                { stat.value }
                </p>
            < p className = "text-white/50 text-xs" >
            { stat.label }
            </p>
            </div>
            ))
        }
            </div>
            </div>

            < div className = "bg-white/5 rounded-2xl p-5" >
                <p className="text-white/80 text-sm italic" >
          & quot;The AI summaries save me hours of reading.& quot;
    </p>
        < p className = "text-white/50 text-xs mt-3" >
            Marcus W. - 48 reviews written
                </p>
                </div>
                </div>
  );
}