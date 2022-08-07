%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% a QUEST handle class 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Written by Yang Zhang
% 2021-Dec-26
classdef quest_APL < handle
    properties
        updatePdf     = [];
        warnPdf       = [];
        normalizePdf  = [];
        tGuess        = [];
        tGuessSd      = [];
        pThreshold    = [];
        beta          = [];
        delta         = [];
        gamma         = [];
        grain         = [];
        dim           = [];
        i             = [];
        x             = [];
        pdf           = [];
        x2            = [];
        p2            = [];
        xThreshold    = [];
        s2            = [];
        trialCount    = [];
        intensity     = [];
        response      = [];
        quantileOrder = [];
        cValue        = [];
        isLog10Trans  = [];
        method        = [];
        minValue      = [];
        maxValue      = [];
        outputRows    = [];
        iUpdate       = 0;
    end

    methods
        function obj= quest_APL(tGuess,tGuessSd,pThreshold,beta,delta,gamma,grain,range,isLog10Trans,maxValue,minValue,method, maxOuputRows)

            obj.updatePdf    = 1; % boolean: 0 for no, 1 for yes
            obj.warnPdf      = 1; % boolean
            obj.normalizePdf = 1; % boolean. This adds a few ms per call to QuestUpdate, but otherwise the pdf will underflow after about 1000 trials.
            obj.tGuess       = tGuess;
            obj.tGuessSd     = tGuessSd;
            obj.pThreshold   = pThreshold;
            obj.beta         = beta;
            obj.delta        = delta;
            obj.gamma        = gamma;
            obj.grain        = grain;
            obj.isLog10Trans = isLog10Trans;
            obj.method       = method;
            obj.maxValue     = maxValue;
            obj.minValue     = minValue;
            obj.outputRows   = zeros(maxOuputRows, 1);

            if isempty(range)
                obj.dim = 500;
            else
                if range <= 0
                    error('"range" must be greater than zero.')
                end
                obj.dim = range/grain;
                obj.dim = 2*ceil(obj.dim/2);	% round up to an even integer
            end
            
            QuestRecompute(obj, 0);

            obj.getQuestValue; % get the first cValue

        end %  end of constructor function
        
        %%%%%%%%%%%%%%%%%%
        % update quest
        %%%%%%%%%%%%%%%%%%
        function updateQuestValue(obj, stimIntensity, response, iOutputRows)
            obj.iUpdate = obj.iUpdate + 1;
            obj.outputRows(obj.iUpdate) = iOutputRows;

            if obj.isLog10Trans
                stimIntensity = log10(stimIntensity);
            end

            QuestUpdate(obj, stimIntensity, response);

            obj.getQuestValue;% get the next cValue
        end

        

        %%%%%%%%%%%%%%%%%%%
        % get quest value
        %%%%%%%%%%%%%%%%%%%
        function getQuestValue(obj)
            % 1,2,3 for quantile, mean, and mode, respectively
            switch obj.method
                case 1
                    obj.cValue = QuestQuantile(obj);
                case 2
                    obj.cValue = QuestMean(obj);
                case 3
                    obj.cValue = QuestMode(obj);
                otherwise
                    error('Quest method should be of [1,2,3] for Quantile, mean, and mode, respectively');
            end

            if obj.isLog10Trans
                obj.cValue = 10^obj.cValue;
            end

            obj.cValue = max(obj.cValue,obj.minValue);
            obj.cValue = min(obj.cValue,obj.maxValue);

        end 


    end % end of methods
end  % end of calss def